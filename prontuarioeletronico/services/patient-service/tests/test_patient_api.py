from fastapi.testclient import TestClient

from src.patient.infra.api.main import _reset_for_tests, app


client = TestClient(app)


def setup_function() -> None:
    _reset_for_tests()


def test_create_patient_success():
    response = client.post(
        "/api/v1/patients",
        json={
            "name": "Maria da Silva",
            "cpf": "12345678901",
            "date_of_birth": "1990-05-15",
            "gender": "F",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["name"] == "Maria da Silva"
    assert body["cpf"] == "12345678901"


def test_get_patient_by_id_success_and_not_found():
    created = client.post(
        "/api/v1/patients",
        json={
            "name": "João Souza",
            "cpf": "10987654321",
            "date_of_birth": "1988-03-09",
            "gender": "M",
        },
    ).json()

    found = client.get(f"/api/v1/patients/{created['id']}")
    assert found.status_code == 200
    assert found.json()["id"] == created["id"]

    not_found = client.get("/api/v1/patients/id-inexistente")
    assert not_found.status_code == 404


def test_list_patients_returns_collection():
    client.post(
        "/api/v1/patients",
        json={
            "name": "Ana Paula",
            "cpf": "11111111111",
            "date_of_birth": "1995-01-21",
            "gender": "F",
        },
    )
    client.post(
        "/api/v1/patients",
        json={
            "name": "Carlos Lima",
            "cpf": "22222222222",
            "date_of_birth": "1992-07-11",
            "gender": "M",
        },
    )

    response = client.get("/api/v1/patients")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2


def test_create_patient_rejects_invalid_cpf():
    response = client.post(
        "/api/v1/patients",
        json={
            "name": "Paciente Teste",
            "cpf": "12345",
            "date_of_birth": "2000-10-10",
            "gender": "F",
        },
    )

    assert response.status_code == 400
    assert "cpf" in response.json()["detail"]