import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


SERVICES_DIR = Path(__file__).resolve().parents[2]
AUTH_SERVICE_ROOT = SERVICES_DIR / "auth-service"
if str(AUTH_SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(AUTH_SERVICE_ROOT))

os.environ.setdefault("AUTH_JWT_SECRET", "test-secret-e2e")
os.environ.setdefault("AUTH_DATABASE_URL", "sqlite:///./test_auth_e2e.db")

from src.auth.infra.api.main import app as auth_app
from src.patient.infra.api import main as patient_main


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


def _login(auth_client: TestClient, username: str, password: str) -> dict:
    response = auth_client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture(autouse=True)
def configure_real_auth_integration():
    auth_client = TestClient(auth_app)
    original_auth_client = patient_main._auth_client

    patient_main._auth_client = LocalAuthServiceClient(auth_client)
    patient_main._reset_for_tests()

    try:
        yield
    finally:
        patient_main._auth_client = original_auth_client
        patient_main._reset_for_tests()


def test_patient_rbac_e2e_with_real_tokens():
    auth_client = TestClient(auth_app)
    patient_client = TestClient(patient_main.app)

    admin_tokens = _login(auth_client, "admin", "admin123")
    professional_tokens = _login(auth_client, "profissional", "prof123")

    create_response = patient_client.post(
        "/api/v1/patients",
        json={
            "name": "Paciente E2E",
            "cpf": "55555555555",
            "date_of_birth": "1991-06-10",
            "gender": "F",
        },
        headers={"Authorization": f"Bearer {professional_tokens['access_token']}"},
    )
    assert create_response.status_code == 201
    patient_id = create_response.json()["id"]

    delete_forbidden = patient_client.delete(
        f"/api/v1/patients/{patient_id}",
        headers={"Authorization": f"Bearer {professional_tokens['access_token']}"},
    )
    assert delete_forbidden.status_code == 403

    delete_admin = patient_client.delete(
        f"/api/v1/patients/{patient_id}",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
    )
    assert delete_admin.status_code == 200
    assert delete_admin.json()["deleted"] is True


def test_patient_rejects_invalid_real_token_e2e():
    patient_client = TestClient(patient_main.app)

    response = patient_client.get(
        "/api/v1/patients",
        headers={"Authorization": "Bearer token-invalido"},
    )
    assert response.status_code == 401