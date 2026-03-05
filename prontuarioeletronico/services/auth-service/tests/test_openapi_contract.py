from fastapi.testclient import TestClient

from src.auth.infra.api.main import app


client = TestClient(app)


def test_openapi_contains_auth_contract_paths():
    response = client.get("/openapi.json")
    assert response.status_code == 200

    spec = response.json()
    paths = spec.get("paths", {})

    assert "/api/v1/auth/login" in paths
    assert "/api/v1/auth/refresh" in paths
    assert "/api/v1/auth/logout" in paths
    assert "/api/v1/auth/verify" in paths
    assert "/api/v1/auth/authorize" in paths


def test_openapi_contains_bearer_security_scheme_and_protected_operations():
    spec = client.get("/openapi.json").json()

    security_schemes = spec.get("components", {}).get("securitySchemes", {})
    assert "HTTPBearer" in security_schemes
    assert security_schemes["HTTPBearer"]["type"] == "http"
    assert security_schemes["HTTPBearer"]["scheme"] == "bearer"

    verify_security = spec["paths"]["/api/v1/auth/verify"]["get"].get("security", [])
    authorize_security = spec["paths"]["/api/v1/auth/authorize"]["get"].get("security", [])
    logout_security = spec["paths"]["/api/v1/auth/logout"]["post"].get("security", [])

    assert {"HTTPBearer": []} in verify_security
    assert {"HTTPBearer": []} in authorize_security
    assert {"HTTPBearer": []} in logout_security


def test_openapi_contains_request_examples_and_security_error_examples():
    spec = client.get("/openapi.json").json()

    login_schema = spec["components"]["schemas"]["LoginRequest"]
    refresh_schema = spec["components"]["schemas"]["RefreshRequest"]
    logout_schema = spec["components"]["schemas"]["LogoutRequest"]

    assert "example" in login_schema
    assert login_schema["example"]["username"] == "admin"
    assert "example" in refresh_schema
    assert "refresh_token" in refresh_schema["example"]
    assert "example" in logout_schema
    assert "refresh_token" in logout_schema["example"]

    verify_401_examples = spec["paths"]["/api/v1/auth/verify"]["get"]["responses"]["401"]["content"]["application/json"]["examples"]
    refresh_401_examples = spec["paths"]["/api/v1/auth/refresh"]["post"]["responses"]["401"]["content"]["application/json"]["examples"]

    assert "revoked" in verify_401_examples
    assert "reused" in refresh_401_examples
