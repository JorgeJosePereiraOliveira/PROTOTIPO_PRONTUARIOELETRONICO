from fastapi.testclient import TestClient

from src.patient.infra.api.main import app


client = TestClient(app)


def test_openapi_contains_required_patient_paths():
    spec = client.get("/openapi.json").json()
    paths = spec.get("paths", {})

    assert "/api/v1/patients" in paths
    assert "/api/v1/patients/{patient_id}" in paths


def test_openapi_contains_create_patient_schema_example():
    spec = client.get("/openapi.json").json()
    schema = spec["components"]["schemas"]["CreatePatientRequest"]

    assert "example" in schema
    assert schema["example"]["name"] == "Maria da Silva"
    assert "cpf" in schema["example"]