from fastapi.testclient import TestClient

from src.professional.infra.api import main


client = TestClient(main.app)
AUTH_HEADER = {"Authorization": "Bearer fake-token"}


def setup_function() -> None:
    main._reset_for_tests()


def _auth_ok(monkeypatch, allowed_roles: set[str] | None = None):
    roles = allowed_roles or {"admin", "profissional"}

    def verify(token: str) -> dict:
        assert token == "fake-token"
        return {"valid": True, "claims": {"sub": "admin-user", "role": "admin"}}

    def authorize(token: str, required_role: str) -> bool:
        assert token == "fake-token"
        return required_role in roles

    monkeypatch.setattr(main._auth_client, "verify", verify)
    monkeypatch.setattr(main._auth_client, "authorize", authorize)


def _auth_invalid(monkeypatch):
    def verify(_token: str) -> dict:
        raise ValueError("invalid token")

    monkeypatch.setattr(main._auth_client, "verify", verify)


def test_create_and_get_professional_success(monkeypatch):
    _auth_ok(monkeypatch, allowed_roles={"admin", "profissional"})

    created = client.post(
        "/api/v1/professionals",
        json={
            "full_name": "Dra. Paula Nunes",
            "document_cpf": "12345678901",
            "council_type": "CRM",
            "council_uf": "SP",
            "council_number": "123456",
            "occupation": "medico",
            "specialty": "clinica medica",
        },
        headers=AUTH_HEADER,
    )
    assert created.status_code == 201
    professional_id = created.json()["id"]

    found = client.get(f"/api/v1/professionals/{professional_id}", headers=AUTH_HEADER)
    assert found.status_code == 200
    assert found.json()["id"] == professional_id
    assert found.json()["status"] == "active"


def test_create_professional_rejects_duplicate_council(monkeypatch):
    _auth_ok(monkeypatch)

    payload = {
        "full_name": "Dr. Joao Silva",
        "document_cpf": "22345678901",
        "council_type": "CRM",
        "council_uf": "RJ",
        "council_number": "445566",
        "occupation": "medico",
    }

    first = client.post("/api/v1/professionals", json=payload, headers=AUTH_HEADER)
    assert first.status_code == 201

    second = client.post("/api/v1/professionals", json=payload, headers=AUTH_HEADER)
    assert second.status_code == 400
    assert "already registered" in second.json()["detail"]


def test_list_and_filter_professionals(monkeypatch):
    _auth_ok(monkeypatch)

    client.post(
        "/api/v1/professionals",
        json={
            "full_name": "Enf. Carla Souza",
            "document_cpf": "32345678901",
            "council_type": "COREN",
            "council_uf": "MG",
            "council_number": "778899",
            "occupation": "enfermeiro",
        },
        headers=AUTH_HEADER,
    )

    response = client.get(
        "/api/v1/professionals",
        params={"council_type": "COREN", "status": "active"},
        headers=AUTH_HEADER,
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["council_type"] == "COREN"


def test_activate_and_deactivate_professional(monkeypatch):
    _auth_ok(monkeypatch)

    created = client.post(
        "/api/v1/professionals",
        json={
            "full_name": "Dra. Camila Prado",
            "document_cpf": "42345678901",
            "council_type": "CRM",
            "council_uf": "PR",
            "council_number": "900123",
            "occupation": "medico",
        },
        headers=AUTH_HEADER,
    )
    professional_id = created.json()["id"]

    deactivated = client.post(
        f"/api/v1/professionals/{professional_id}/deactivate",
        headers=AUTH_HEADER,
    )
    assert deactivated.status_code == 200
    assert deactivated.json()["status"] == "inactive"

    activated = client.post(
        f"/api/v1/professionals/{professional_id}/activate",
        headers=AUTH_HEADER,
    )
    assert activated.status_code == 200
    assert activated.json()["status"] == "active"


def test_mutation_endpoints_require_admin(monkeypatch):
    _auth_ok(monkeypatch, allowed_roles={"profissional"})

    response = client.post(
        "/api/v1/professionals",
        json={
            "full_name": "Dr. Sem Permissao",
            "document_cpf": "52345678901",
            "council_type": "CRM",
            "council_uf": "BA",
            "council_number": "456789",
            "occupation": "medico",
        },
        headers=AUTH_HEADER,
    )
    assert response.status_code == 403


def test_protected_endpoints_reject_invalid_token(monkeypatch):
    _auth_invalid(monkeypatch)

    response = client.get("/api/v1/professionals", headers=AUTH_HEADER)
    assert response.status_code == 401


def test_audit_events_emitted_for_create_and_status_changes(monkeypatch):
    _auth_ok(monkeypatch)
    captured_events: list[tuple[str, dict]] = []

    def create_event(*, token: str, payload: dict) -> dict:
        captured_events.append((token, payload))
        return {"id": f"event-{len(captured_events)}"}

    monkeypatch.setattr(main._audit_client, "create_event", create_event)

    created = client.post(
        "/api/v1/professionals",
        json={
            "full_name": "Dra. Juliana Lemos",
            "document_cpf": "62345678901",
            "council_type": "CRM",
            "council_uf": "SC",
            "council_number": "333222",
            "occupation": "medico",
        },
        headers=AUTH_HEADER,
    )
    assert created.status_code == 201
    professional_id = created.json()["id"]

    deactivated = client.post(
        f"/api/v1/professionals/{professional_id}/deactivate",
        headers=AUTH_HEADER,
    )
    assert deactivated.status_code == 200

    assert len(captured_events) == 2
    assert captured_events[0][1]["operation"] == "create_professional"
    assert captured_events[1][1]["operation"] == "deactivate_professional"
