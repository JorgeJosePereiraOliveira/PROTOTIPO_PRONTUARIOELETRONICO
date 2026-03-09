import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient


SERVICES_DIR = Path(__file__).resolve().parents[2]
AUTH_SERVICE_ROOT = SERVICES_DIR / "auth-service"
PATIENT_SERVICE_ROOT = SERVICES_DIR / "patient-service"
EMR_SERVICE_ROOT = SERVICES_DIR / "emr-service"

if str(AUTH_SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(AUTH_SERVICE_ROOT))
if str(PATIENT_SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(PATIENT_SERVICE_ROOT))
if str(EMR_SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(EMR_SERVICE_ROOT))

os.environ.setdefault("AUTH_JWT_SECRET", "test-secret-gateway")
os.environ.setdefault("AUTH_DATABASE_URL", "sqlite:///./test_auth_gateway.db")
os.environ.setdefault("PATIENT_DATABASE_URL", "sqlite:///./test_patient_gateway.db")
os.environ.setdefault("EMR_DATABASE_URL", "sqlite:///./test_emr_gateway.db")

from src.auth.infra.api.main import app as auth_app
from src.emr.infra.api import main as emr_main
from src.patient.infra.api import main as patient_main
from src.gateway.infra.api import main as gateway_main


class LocalServiceProxy:
    def __init__(self, client: TestClient):
        self._client = client

    def request(
        self,
        method: str,
        path: str,
        authorization: str | None = None,
        json_body: dict | None = None,
        params: dict | None = None,
    ) -> tuple[int, object]:
        headers = {}
        if authorization:
            headers["Authorization"] = authorization

        response = self._client.request(
            method=method,
            url=path,
            headers=headers,
            json=json_body,
            params=params,
        )
        try:
            body = response.json()
        except ValueError:
            body = {"detail": response.text}
        return response.status_code, body


class LocalAuthServiceClient:
    def __init__(self, auth_client: TestClient):
        self._auth_client = auth_client

    def verify(self, token: str) -> dict:
        response = self._auth_client.get(
            "/api/v1/auth/verify",
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code >= 400:
            raise ValueError(response.json().get("detail", "invalid token"))
        return response.json()

    def authorize(self, token: str, required_role: str) -> bool:
        response = self._auth_client.get(
            "/api/v1/auth/authorize",
            params={"required_role": required_role},
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code >= 400:
            raise ValueError(response.json().get("detail", "unauthorized"))
        return bool(response.json().get("authorized"))


def setup_function() -> None:
    auth_client = TestClient(auth_app)
    patient_main._auth_client = LocalAuthServiceClient(auth_client)
    emr_main._auth_client = LocalAuthServiceClient(auth_client)
    patient_main._reset_for_tests()
    emr_main._reset_for_tests()

    gateway_main._auth_proxy = LocalServiceProxy(auth_client)
    gateway_main._patient_proxy = LocalServiceProxy(TestClient(patient_main.app))
    gateway_main._emr_proxy = LocalServiceProxy(TestClient(emr_main.app))


def _gateway_login(client: TestClient, username: str, password: str) -> dict:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    return response.json()


def test_gateway_end_to_end_auth_and_patient_flow():
    gateway_client = TestClient(gateway_main.app)

    admin_tokens = _gateway_login(gateway_client, "admin", "admin123")
    prof_tokens = _gateway_login(gateway_client, "profissional", "prof123")

    create_response = gateway_client.post(
        "/api/v1/patients",
        json={
            "name": "Paciente Gateway",
            "cpf": "66666666666",
            "date_of_birth": "1993-08-11",
            "gender": "F",
        },
        headers={"Authorization": f"Bearer {prof_tokens['access_token']}"},
    )
    assert create_response.status_code == 201
    patient_id = create_response.json()["id"]

    list_response = gateway_client.get(
        "/api/v1/patients",
        headers={"Authorization": f"Bearer {prof_tokens['access_token']}"},
    )
    assert list_response.status_code == 200
    assert isinstance(list_response.json(), list)
    assert len(list_response.json()) == 1

    update_response = gateway_client.put(
        f"/api/v1/patients/{patient_id}",
        json={
            "name": "Paciente Gateway Atualizado",
            "cpf": "66666666666",
            "date_of_birth": "1993-08-11",
            "gender": "F",
        },
        headers={"Authorization": f"Bearer {prof_tokens['access_token']}"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Paciente Gateway Atualizado"

    forbidden_delete = gateway_client.delete(
        f"/api/v1/patients/{patient_id}",
        headers={"Authorization": f"Bearer {prof_tokens['access_token']}"},
    )
    assert forbidden_delete.status_code == 403

    allowed_delete = gateway_client.delete(
        f"/api/v1/patients/{patient_id}",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
    )
    assert allowed_delete.status_code == 200
    assert allowed_delete.json()["deleted"] is True


def test_gateway_end_to_end_emr_flow():
    gateway_client = TestClient(gateway_main.app)
    prof_tokens = _gateway_login(gateway_client, "profissional", "prof123")
    auth_header = {"Authorization": f"Bearer {prof_tokens['access_token']}"}

    create_problem = gateway_client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-gw-emr-1",
            "description": "DPOC em acompanhamento",
            "status": "active",
        },
        headers=auth_header,
    )
    assert create_problem.status_code == 201
    problem_id = create_problem.json()["id"]

    get_problem = gateway_client.get(
        f"/api/v1/emr/problems/{problem_id}",
        headers=auth_header,
    )
    assert get_problem.status_code == 200
    assert get_problem.json()["id"] == problem_id

    create_soap = gateway_client.post(
        "/api/v1/emr/soap",
        json={
            "problem_id": problem_id,
            "patient_id": "patient-gw-emr-1",
            "professional_id": "prof-gateway-1",
            "subjective": "Paciente com dispneia aos esforcos moderados.",
            "objective": "Ausculta com sibilos esparsos.",
            "assessment": "DPOC estavel, sem sinais de exacerbacao aguda.",
            "plan": "Manter broncodilatador e reforcar cessacao do tabagismo.",
        },
        headers=auth_header,
    )
    assert create_soap.status_code == 201
    soap_id = create_soap.json()["id"]

    get_soap = gateway_client.get(f"/api/v1/emr/soap/{soap_id}", headers=auth_header)
    assert get_soap.status_code == 200
    assert get_soap.json()["problem_id"] == problem_id


def test_gateway_rejects_missing_or_invalid_token():
    gateway_client = TestClient(gateway_main.app)

    missing_auth = gateway_client.get("/api/v1/patients")
    assert missing_auth.status_code == 401

    invalid_auth = gateway_client.get(
        "/api/v1/patients",
        headers={"Authorization": "Bearer token-invalido"},
    )
    assert invalid_auth.status_code == 401