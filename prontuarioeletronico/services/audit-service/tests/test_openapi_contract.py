from fastapi.testclient import TestClient

from src.audit.infra.api.main import app


client = TestClient(app)


def test_openapi_contains_required_audit_paths():
    spec = client.get("/openapi.json").json()
    paths = spec.get("paths", {})

    assert "/api/v1/audit/events" in paths
    assert "/api/v1/audit/events/{event_id}" in paths
    assert "post" in paths["/api/v1/audit/events"]
    assert "get" in paths["/api/v1/audit/events"]
    assert "get" in paths["/api/v1/audit/events/{event_id}"]


def test_openapi_contains_create_audit_schema_example():
    spec = client.get("/openapi.json").json()
    schema = spec["components"]["schemas"]["CreateAuditEventRequest"]

    assert "example" in schema
    assert schema["example"]["context"] == "emr"
    assert schema["example"]["status"] == "success"


def test_openapi_contains_bearer_security_for_audit_operations():
    spec = client.get("/openapi.json").json()

    security_schemes = spec.get("components", {}).get("securitySchemes", {})
    assert "HTTPBearer" in security_schemes

    events_post = spec["paths"]["/api/v1/audit/events"]["post"].get("security", [])
    events_get = spec["paths"]["/api/v1/audit/events"]["get"].get("security", [])
    event_get = spec["paths"]["/api/v1/audit/events/{event_id}"]["get"].get(
        "security", []
    )

    assert {"HTTPBearer": []} in events_post
    assert {"HTTPBearer": []} in events_get
    assert {"HTTPBearer": []} in event_get
