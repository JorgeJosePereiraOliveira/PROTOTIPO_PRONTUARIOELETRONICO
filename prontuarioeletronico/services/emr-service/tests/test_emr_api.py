from fastapi.testclient import TestClient

from src.emr.infra.api import main


client = TestClient(main.app)
AUTH_HEADER = {"Authorization": "Bearer fake-token"}


def setup_function() -> None:
    main._reset_for_tests()


def _auth_ok(monkeypatch, allowed_roles: set[str] | None = None):
    roles = allowed_roles or {"admin", "profissional"}

    def verify(token: str) -> dict:
        assert token == "fake-token"
        return {"valid": True, "claims": {"sub": "1"}}

    def authorize(token: str, required_role: str) -> bool:
        assert token == "fake-token"
        return required_role in roles

    monkeypatch.setattr(main._auth_client, "verify", verify)
    monkeypatch.setattr(main._auth_client, "authorize", authorize)


def _auth_invalid(monkeypatch):
    def verify(_token: str) -> dict:
        raise ValueError("invalid token")

    monkeypatch.setattr(main._auth_client, "verify", verify)


def test_create_problem_and_find_problem(monkeypatch):
    _auth_ok(monkeypatch)

    create_response = client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-100",
            "description": "Diabetes mellitus tipo 2",
            "status": "active",
        },
        headers=AUTH_HEADER,
    )
    assert create_response.status_code == 201
    problem = create_response.json()
    assert problem["id"]

    get_response = client.get(
        f"/api/v1/emr/problems/{problem['id']}",
        headers=AUTH_HEADER,
    )
    assert get_response.status_code == 200
    assert get_response.json()["description"] == "Diabetes mellitus tipo 2"


def test_create_soap_and_find_soap(monkeypatch):
    _auth_ok(monkeypatch)

    problem = client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-101",
            "description": "Asma persistente",
            "status": "active",
        },
        headers=AUTH_HEADER,
    ).json()

    soap_response = client.post(
        "/api/v1/emr/soap",
        json={
            "problem_id": problem["id"],
            "patient_id": "patient-101",
            "professional_id": "prof-01",
            "subjective": "Paciente refere dispneia noturna frequente.",
            "objective": "Saturacao de O2 em 94% em repouso.",
            "assessment": "Asma parcialmente controlada.",
            "plan": "Ajustar corticoide inalatorio e retorno em 15 dias.",
        },
        headers=AUTH_HEADER,
    )
    assert soap_response.status_code == 201
    soap = soap_response.json()

    get_response = client.get(f"/api/v1/emr/soap/{soap['id']}", headers=AUTH_HEADER)
    assert get_response.status_code == 200
    assert get_response.json()["problem_id"] == problem["id"]


def test_create_soap_rejects_missing_problem(monkeypatch):
    _auth_ok(monkeypatch)

    response = client.post(
        "/api/v1/emr/soap",
        json={
            "problem_id": "problem-inexistente",
            "patient_id": "patient-200",
            "professional_id": "prof-02",
            "subjective": "Queixa de dor lombar.",
            "objective": "Dor a palpacao em regiao lombar.",
            "assessment": "Lombalgia mecanica.",
            "plan": "Analgesico e orientacao postural.",
        },
        headers=AUTH_HEADER,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "problem not found"


def test_protected_endpoints_reject_invalid_token(monkeypatch):
    _auth_invalid(monkeypatch)

    response = client.get("/api/v1/emr/problems/problem-1", headers=AUTH_HEADER)
    assert response.status_code == 401


def test_protected_endpoints_reject_insufficient_role(monkeypatch):
    _auth_ok(monkeypatch, allowed_roles={"recepcao"})

    response = client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-300",
            "description": "Enxaqueca cronica",
            "status": "active",
        },
        headers=AUTH_HEADER,
    )
    assert response.status_code == 403
