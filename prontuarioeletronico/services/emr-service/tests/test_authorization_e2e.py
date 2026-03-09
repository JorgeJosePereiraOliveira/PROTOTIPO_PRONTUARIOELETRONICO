import os
import sys
from pathlib import Path
import importlib

import pytest
from fastapi.testclient import TestClient


SERVICES_DIR = Path(__file__).resolve().parents[2]
AUTH_SERVICE_ROOT = SERVICES_DIR / "auth-service"
if str(AUTH_SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(AUTH_SERVICE_ROOT))

os.environ.setdefault("AUTH_JWT_SECRET", "test-secret-emr-e2e")
os.environ.setdefault("AUTH_DATABASE_URL", "sqlite:///./test_auth_emr_e2e.db")
os.environ.setdefault("EMR_DATABASE_URL", "sqlite:///./test_emr_e2e.db")

auth_main = importlib.import_module("src.auth.infra.api.main")
emr_main = importlib.import_module("src.emr.infra.api.main")
auth_app = auth_main.app


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
    original_auth_client = emr_main._auth_client

    emr_main._auth_client = LocalAuthServiceClient(auth_client)
    emr_main._reset_for_tests()

    try:
        yield
    finally:
        emr_main._auth_client = original_auth_client
        emr_main._reset_for_tests()


def test_emr_rbac_e2e_with_real_tokens():
    auth_client = TestClient(auth_app)
    emr_client = TestClient(emr_main.app)

    professional_tokens = _login(auth_client, "profissional", "prof123")

    create_problem = emr_client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-e2e-1",
            "description": "Insuficiencia cardiaca cronica",
            "status": "active",
        },
        headers={"Authorization": f"Bearer {professional_tokens['access_token']}"},
    )
    assert create_problem.status_code == 201
    problem_id = create_problem.json()["id"]

    create_soap = emr_client.post(
        "/api/v1/emr/soap",
        json={
            "problem_id": problem_id,
            "patient_id": "patient-e2e-1",
            "professional_id": "prof-e2e-1",
            "subjective": "Paciente relata fadiga aos pequenos esforcos.",
            "objective": "Edema maleolar bilateral leve.",
            "assessment": "Insuficiencia cardiaca compensada parcialmente.",
            "plan": "Ajuste de diuretico e monitorar peso diario.",
        },
        headers={"Authorization": f"Bearer {professional_tokens['access_token']}"},
    )
    assert create_soap.status_code == 201


def test_emr_rejects_invalid_real_token_e2e():
    emr_client = TestClient(emr_main.app)

    response = emr_client.get(
        "/api/v1/emr/problems/problem-invalido",
        headers={"Authorization": "Bearer token-invalido"},
    )
    assert response.status_code == 401
