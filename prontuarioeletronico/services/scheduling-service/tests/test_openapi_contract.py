from fastapi.testclient import TestClient

from src.scheduling.infra.api.main import app


client = TestClient(app)


def test_openapi_contains_required_scheduling_paths():
    spec = client.get("/openapi.json").json()
    paths = spec.get("paths", {})

    assert "/api/v1/scheduling/appointments" in paths
    assert "/api/v1/scheduling/appointments/{appointment_id}" in paths
    assert "post" in paths["/api/v1/scheduling/appointments"]
    assert "get" in paths["/api/v1/scheduling/appointments"]
    assert "get" in paths["/api/v1/scheduling/appointments/{appointment_id}"]
    assert "delete" in paths["/api/v1/scheduling/appointments/{appointment_id}"]


def test_openapi_contains_create_appointment_schema_example():
    spec = client.get("/openapi.json").json()
    schema = spec["components"]["schemas"]["CreateAppointmentRequest"]

    assert "example" in schema
    assert schema["example"]["patient_id"] == "patient-123"
    assert "scheduled_at" in schema["example"]


def test_openapi_contains_bearer_security_for_scheduling_operations():
    spec = client.get("/openapi.json").json()

    security_schemes = spec.get("components", {}).get("securitySchemes", {})
    assert "HTTPBearer" in security_schemes

    appointments_post = spec["paths"]["/api/v1/scheduling/appointments"]["post"].get(
        "security", []
    )
    appointments_get = spec["paths"]["/api/v1/scheduling/appointments"]["get"].get(
        "security", []
    )
    appointment_get = spec["paths"]["/api/v1/scheduling/appointments/{appointment_id}"][
        "get"
    ].get("security", [])
    appointment_delete = spec["paths"][
        "/api/v1/scheduling/appointments/{appointment_id}"
    ]["delete"].get("security", [])

    assert {"HTTPBearer": []} in appointments_post
    assert {"HTTPBearer": []} in appointments_get
    assert {"HTTPBearer": []} in appointment_get
    assert {"HTTPBearer": []} in appointment_delete
