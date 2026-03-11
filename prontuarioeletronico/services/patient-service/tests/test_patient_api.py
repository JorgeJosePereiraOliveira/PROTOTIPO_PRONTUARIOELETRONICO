from fastapi.testclient import TestClient

from src.patient.infra.api import main


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


def test_create_patient_success(monkeypatch):
    _auth_ok(monkeypatch)
    response = client.post(
        "/api/v1/patients",
        json={
            "name": "Maria da Silva",
            "cpf": "12345678901",
            "date_of_birth": "1990-05-15",
            "gender": "F",
        },
        headers=AUTH_HEADER,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["name"] == "Maria da Silva"
    assert body["cpf"] == "12345678901"


def test_get_patient_by_id_success_and_not_found(monkeypatch):
    _auth_ok(monkeypatch)
    created = client.post(
        "/api/v1/patients",
        json={
            "name": "João Souza",
            "cpf": "10987654321",
            "date_of_birth": "1988-03-09",
            "gender": "M",
        },
        headers=AUTH_HEADER,
    ).json()

    found = client.get(f"/api/v1/patients/{created['id']}", headers=AUTH_HEADER)
    assert found.status_code == 200
    assert found.json()["id"] == created["id"]

    not_found = client.get("/api/v1/patients/id-inexistente", headers=AUTH_HEADER)
    assert not_found.status_code == 404


def test_list_patients_returns_collection(monkeypatch):
    _auth_ok(monkeypatch)
    client.post(
        "/api/v1/patients",
        json={
            "name": "Ana Paula",
            "cpf": "11111111111",
            "date_of_birth": "1995-01-21",
            "gender": "F",
        },
        headers=AUTH_HEADER,
    )
    client.post(
        "/api/v1/patients",
        json={
            "name": "Carlos Lima",
            "cpf": "22222222222",
            "date_of_birth": "1992-07-11",
            "gender": "M",
        },
        headers=AUTH_HEADER,
    )

    response = client.get("/api/v1/patients", headers=AUTH_HEADER)

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2


def test_create_patient_rejects_invalid_cpf(monkeypatch):
    _auth_ok(monkeypatch)
    response = client.post(
        "/api/v1/patients",
        json={
            "name": "Paciente Teste",
            "cpf": "12345",
            "date_of_birth": "2000-10-10",
            "gender": "F",
        },
        headers=AUTH_HEADER,
    )

    assert response.status_code == 400
    assert "cpf" in response.json()["detail"]


def test_update_patient_success(monkeypatch):
    _auth_ok(monkeypatch)
    created = client.post(
        "/api/v1/patients",
        json={
            "name": "Bruna Lima",
            "cpf": "33333333333",
            "date_of_birth": "1997-04-20",
            "gender": "F",
        },
        headers=AUTH_HEADER,
    ).json()

    response = client.put(
        f"/api/v1/patients/{created['id']}",
        json={
            "name": "Bruna Lima Atualizada",
            "cpf": "33333333333",
            "date_of_birth": "1997-04-20",
            "gender": "F",
        },
        headers=AUTH_HEADER,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Bruna Lima Atualizada"


def test_delete_patient_requires_admin_role(monkeypatch):
    _auth_ok(monkeypatch, allowed_roles={"profissional"})
    created = client.post(
        "/api/v1/patients",
        json={
            "name": "Paulo Tavares",
            "cpf": "44444444444",
            "date_of_birth": "1985-12-01",
            "gender": "M",
        },
        headers=AUTH_HEADER,
    ).json()

    forbidden = client.delete(f"/api/v1/patients/{created['id']}", headers=AUTH_HEADER)
    assert forbidden.status_code == 403


def test_protected_endpoints_reject_invalid_token(monkeypatch):
    _auth_invalid(monkeypatch)

    response = client.get("/api/v1/patients", headers=AUTH_HEADER)
    assert response.status_code == 401


def test_create_and_revoke_consent_with_audit(monkeypatch):
    _auth_ok(monkeypatch)
    captured_events: list[tuple[str, dict]] = []

    def create_event(token: str, payload: dict) -> dict:
        captured_events.append((token, payload))
        return {"id": f"event-{len(captured_events)}"}

    monkeypatch.setattr(main._audit_client, "create_event", create_event)

    created_patient = client.post(
        "/api/v1/patients",
        json={
            "name": "Paciente Consentimento",
            "cpf": "77777777777",
            "date_of_birth": "1990-10-10",
            "gender": "F",
        },
        headers=AUTH_HEADER,
    ).json()

    create_consent = client.post(
        f"/api/v1/patients/{created_patient['id']}/consents",
        json={
            "legal_basis": "consentimento",
            "purpose": "Uso de dados para continuidade assistencial",
        },
        headers=AUTH_HEADER,
    )
    assert create_consent.status_code == 201
    consent = create_consent.json()
    assert consent["status"] == "active"

    revoke = client.post(
        f"/api/v1/patients/{created_patient['id']}/consents/{consent['id']}/revoke",
        headers=AUTH_HEADER,
    )
    assert revoke.status_code == 200
    assert revoke.json()["status"] == "revoked"
    assert revoke.json()["revoked_at"] is not None

    assert len(captured_events) == 2
    assert captured_events[0][1]["operation"] == "create_consent"
    assert captured_events[0][1]["status"] == "success"
    assert captured_events[1][1]["operation"] == "revoke_consent"
    assert captured_events[1][1]["status"] == "success"


def test_create_consent_rejects_unknown_patient(monkeypatch):
    _auth_ok(monkeypatch)

    def create_event(*, token: str, payload: dict) -> dict:
        return {"id": "event-x", "token": token, "payload": payload}

    monkeypatch.setattr(main._audit_client, "create_event", create_event)

    response = client.post(
        "/api/v1/patients/patient-inexistente/consents",
        json={
            "legal_basis": "consentimento",
            "purpose": "Compartilhamento de dados",
        },
        headers=AUTH_HEADER,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "patient not found"