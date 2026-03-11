from fastapi.testclient import TestClient

from src.emr.infra.api.main import app


client = TestClient(app)


def test_openapi_contains_required_emr_paths():
    spec = client.get("/openapi.json").json()
    paths = spec.get("paths", {})

    assert "/api/v1/emr/problems" in paths
    assert "/api/v1/emr/problems/{problem_id}" in paths
    assert "/api/v1/emr/soap" in paths
    assert "/api/v1/emr/soap/{soap_id}" in paths
    assert "/api/v1/emr/terminology/validate" in paths


def test_openapi_contains_schema_examples():
    spec = client.get("/openapi.json").json()

    problem_schema = spec["components"]["schemas"]["CreateProblemRequest"]
    soap_schema = spec["components"]["schemas"]["CreateSOAPRequest"]

    assert "example" in problem_schema
    assert "patient_id" in problem_schema["example"]
    assert "example" in soap_schema
    assert "subjective" in soap_schema["example"]


def test_openapi_contains_bearer_security_for_emr_operations():
    spec = client.get("/openapi.json").json()

    security_schemes = spec.get("components", {}).get("securitySchemes", {})
    assert "HTTPBearer" in security_schemes

    problem_post = spec["paths"]["/api/v1/emr/problems"]["post"].get("security", [])
    problem_get = spec["paths"]["/api/v1/emr/problems/{problem_id}"]["get"].get(
        "security", []
    )
    soap_post = spec["paths"]["/api/v1/emr/soap"]["post"].get("security", [])
    soap_get = spec["paths"]["/api/v1/emr/soap/{soap_id}"]["get"].get("security", [])

    assert {"HTTPBearer": []} in problem_post
    assert {"HTTPBearer": []} in problem_get
    assert {"HTTPBearer": []} in soap_post
    assert {"HTTPBearer": []} in soap_get
