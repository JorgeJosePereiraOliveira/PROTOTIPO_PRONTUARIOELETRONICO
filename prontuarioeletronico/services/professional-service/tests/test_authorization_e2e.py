import os
import sys
import importlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


SERVICES_DIR = Path(__file__).resolve().parents[2]
AUTH_SERVICE_ROOT = SERVICES_DIR / "auth-service"
if str(AUTH_SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(AUTH_SERVICE_ROOT))

os.environ.setdefault("AUTH_JWT_SECRET", "test-secret-prof-e2e")
os.environ.setdefault("AUTH_DATABASE_URL", "sqlite:///./test_auth_prof_e2e.db")

auth_app = importlib.import_module("src.auth.infra.api.main").app
professional_main = importlib.import_module("src.professional.infra.api.main")


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
    original_auth_client = professional_main._auth_client

    professional_main._auth_client = LocalAuthServiceClient(auth_client)
    professional_main._reset_for_tests()

    try:
        yield
    finally:
        professional_main._auth_client = original_auth_client
        professional_main._reset_for_tests()


def test_professional_rbac_e2e_with_real_tokens():
    auth_client = TestClient(auth_app)
    professional_client = TestClient(professional_main.app)

    admin_tokens = _login(auth_client, "admin", "admin123")
    professional_tokens = _login(auth_client, "profissional", "prof123")

    forbidden_create = professional_client.post(
        "/api/v1/professionals",
        json={
            "full_name": "Dr. E2E Restrito",
            "document_cpf": "72345678901",
            "council_type": "CRM",
            "council_uf": "SP",
            "council_number": "112233",
            "occupation": "medico",
        },
        headers={"Authorization": f"Bearer {professional_tokens['access_token']}"},
    )
    assert forbidden_create.status_code == 403

    create_response = professional_client.post(
        "/api/v1/professionals",
        json={
            "full_name": "Dr. E2E Permitido",
            "document_cpf": "82345678901",
            "council_type": "CRM",
            "council_uf": "SP",
            "council_number": "224466",
            "occupation": "medico",
        },
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
    )
    assert create_response.status_code == 201
    professional_id = create_response.json()["id"]

    list_response = professional_client.get(
        "/api/v1/professionals",
        headers={"Authorization": f"Bearer {professional_tokens['access_token']}"},
    )
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    deactivate_response = professional_client.post(
        f"/api/v1/professionals/{professional_id}/deactivate",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
    )
    assert deactivate_response.status_code == 200
    assert deactivate_response.json()["status"] == "inactive"


def test_professional_rejects_invalid_real_token_e2e():
    professional_client = TestClient(professional_main.app)

    response = professional_client.get(
        "/api/v1/professionals",
        headers={"Authorization": "Bearer token-invalido"},
    )
    assert response.status_code == 401
