from fastapi.testclient import TestClient

from src.patient.infra.api.main import app


client = TestClient(app)


def test_openapi_contains_required_patient_paths():
    spec = client.get("/openapi.json").json()
    paths = spec.get("paths", {})

    assert "/api/v1/patients" in paths
    assert "/api/v1/patients/{patient_id}" in paths
    assert "/api/v1/patients/{patient_id}/consents" in paths
    assert "/api/v1/patients/{patient_id}/consents/{consent_id}/revoke" in paths
    assert "put" in paths["/api/v1/patients/{patient_id}"]
    assert "delete" in paths["/api/v1/patients/{patient_id}"]


def test_openapi_contains_create_patient_schema_example():
    spec = client.get("/openapi.json").json()
    schema = spec["components"]["schemas"]["CreatePatientRequest"]

    assert "example" in schema
    assert schema["example"]["name"] == "Maria da Silva"
    assert "cpf" in schema["example"]


def test_openapi_contains_bearer_security_for_patient_operations():
    spec = client.get("/openapi.json").json()

    security_schemes = spec.get("components", {}).get("securitySchemes", {})
    assert "HTTPBearer" in security_schemes

    patients_post = spec["paths"]["/api/v1/patients"]["post"].get("security", [])
    patients_get = spec["paths"]["/api/v1/patients"]["get"].get("security", [])
    patient_put = spec["paths"]["/api/v1/patients/{patient_id}"]["put"].get("security", [])
    patient_delete = spec["paths"]["/api/v1/patients/{patient_id}"]["delete"].get("security", [])
    consent_post = spec["paths"]["/api/v1/patients/{patient_id}/consents"]["post"].get("security", [])
    consent_list = spec["paths"]["/api/v1/patients/{patient_id}/consents"]["get"].get("security", [])
    consent_revoke = spec["paths"]["/api/v1/patients/{patient_id}/consents/{consent_id}/revoke"]["post"].get("security", [])

    assert {"HTTPBearer": []} in patients_post
    assert {"HTTPBearer": []} in patients_get
    assert {"HTTPBearer": []} in patient_put
    assert {"HTTPBearer": []} in patient_delete
    assert {"HTTPBearer": []} in consent_post
    assert {"HTTPBearer": []} in consent_list
    assert {"HTTPBearer": []} in consent_revoke