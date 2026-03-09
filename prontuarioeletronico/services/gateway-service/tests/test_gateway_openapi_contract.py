from fastapi.testclient import TestClient

from src.gateway.infra.api.main import app


client = TestClient(app)


def test_openapi_contains_gateway_auth_and_patient_paths():
    spec = client.get("/openapi.json").json()
    paths = spec.get("paths", {})

    assert "/api/v1/auth/login" in paths
    assert "/api/v1/auth/refresh" in paths
    assert "/api/v1/auth/logout" in paths
    assert "/api/v1/auth/verify" in paths
    assert "/api/v1/auth/authorize" in paths

    assert "/api/v1/patients" in paths
    assert "/api/v1/patients/{patient_id}" in paths
    assert "post" in paths["/api/v1/patients"]
    assert "get" in paths["/api/v1/patients"]
    assert "put" in paths["/api/v1/patients/{patient_id}"]
    assert "delete" in paths["/api/v1/patients/{patient_id}"]

    assert "/api/v1/emr/problems" in paths
    assert "/api/v1/emr/problems/{problem_id}" in paths
    assert "/api/v1/emr/soap" in paths
    assert "/api/v1/emr/soap/{soap_id}" in paths


def test_openapi_contains_login_schema_example():
    spec = client.get("/openapi.json").json()
    schema = spec["components"]["schemas"]["LoginRequest"]

    assert "example" in schema
    assert schema["example"]["username"] == "admin"