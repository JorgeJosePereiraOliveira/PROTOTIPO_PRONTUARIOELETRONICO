from fastapi.testclient import TestClient

from src.auth.infra.api.main import app


client = TestClient(app)


def test_login_endpoint_returns_jwt_token_for_admin():
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["role"] == "admin"
    assert body["access_token"]
    assert body["refresh_token"]


def test_refresh_endpoint_rotates_refresh_token():
    login_response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    initial_refresh_token = login_response.json()["refresh_token"]

    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": initial_refresh_token},
    )

    assert refresh_response.status_code == 200
    body = refresh_response.json()
    assert body["access_token"]
    assert body["refresh_token"]
    assert body["refresh_token"] != initial_refresh_token


def test_refresh_endpoint_rejects_reused_refresh_token():
    login_response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    initial_refresh_token = login_response.json()["refresh_token"]

    first_refresh = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": initial_refresh_token},
    )
    assert first_refresh.status_code == 200

    second_refresh = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": initial_refresh_token},
    )
    assert second_refresh.status_code == 401


def test_verify_endpoint_accepts_valid_token():
    login_response = client.post(
        "/api/v1/auth/login",
        json={"username": "profissional", "password": "prof123"},
    )
    token = login_response.json()["access_token"]

    verify_response = client.get(
        "/api/v1/auth/verify",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert verify_response.status_code == 200
    body = verify_response.json()
    assert body["valid"] is True
    assert body["claims"]["role"] == "profissional"


def test_authorize_endpoint_denies_professional_for_admin_resource():
    login_response = client.post(
        "/api/v1/auth/login",
        json={"username": "profissional", "password": "prof123"},
    )
    token = login_response.json()["access_token"]

    authorize_response = client.get(
        "/api/v1/auth/authorize",
        params={"required_role": "admin"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert authorize_response.status_code == 200
    body = authorize_response.json()
    assert body["authorized"] is False
    assert body["role"] == "profissional"
