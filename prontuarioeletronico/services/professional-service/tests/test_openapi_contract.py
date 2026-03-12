from fastapi.testclient import TestClient

from src.professional.infra.api.main import app


client = TestClient(app)


def test_openapi_contains_required_professional_paths():
    spec = client.get("/openapi.json").json()
    paths = spec.get("paths", {})

    assert "/api/v1/professionals" in paths
    assert "/api/v1/professionals/{professional_id}" in paths
    assert "/api/v1/professionals/{professional_id}/activate" in paths
    assert "/api/v1/professionals/{professional_id}/deactivate" in paths


def test_openapi_contains_create_professional_schema_example():
    spec = client.get("/openapi.json").json()
    schema = spec["components"]["schemas"]["CreateProfessionalRequest"]

    assert "example" in schema
    assert schema["example"]["council_type"] == "CRM"
    assert "full_name" in schema["example"]


def test_openapi_contains_bearer_security_for_professional_operations():
    spec = client.get("/openapi.json").json()

    security_schemes = spec.get("components", {}).get("securitySchemes", {})
    assert "HTTPBearer" in security_schemes

    create_op = spec["paths"]["/api/v1/professionals"]["post"].get("security", [])
    list_op = spec["paths"]["/api/v1/professionals"]["get"].get("security", [])
    get_op = spec["paths"]["/api/v1/professionals/{professional_id}"]["get"].get(
        "security", []
    )
    activate_op = spec["paths"]["/api/v1/professionals/{professional_id}/activate"][
        "post"
    ].get("security", [])
    deactivate_op = spec["paths"][
        "/api/v1/professionals/{professional_id}/deactivate"
    ]["post"].get("security", [])

    assert {"HTTPBearer": []} in create_op
    assert {"HTTPBearer": []} in list_op
    assert {"HTTPBearer": []} in get_op
    assert {"HTTPBearer": []} in activate_op
    assert {"HTTPBearer": []} in deactivate_op
