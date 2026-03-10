from fastapi.testclient import TestClient

from src.scheduling.infra.api import main


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


def test_create_get_list_and_delete_appointment(monkeypatch):
    _auth_ok(monkeypatch)

    create_response = client.post(
        "/api/v1/scheduling/appointments",
        json={
            "patient_id": "patient-1",
            "professional_id": "professional-1",
            "scheduled_at": "2026-03-20T10:30:00Z",
            "reason": "Consulta de retorno",
        },
        headers=AUTH_HEADER,
    )
    assert create_response.status_code == 201
    appointment_id = create_response.json()["id"]

    get_response = client.get(
        f"/api/v1/scheduling/appointments/{appointment_id}",
        headers=AUTH_HEADER,
    )
    assert get_response.status_code == 200
    assert get_response.json()["patient_id"] == "patient-1"

    list_response = client.get("/api/v1/scheduling/appointments", headers=AUTH_HEADER)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    delete_response = client.delete(
        f"/api/v1/scheduling/appointments/{appointment_id}",
        headers=AUTH_HEADER,
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["deleted"] is True


def test_rejects_invalid_scheduled_at(monkeypatch):
    _auth_ok(monkeypatch)

    response = client.post(
        "/api/v1/scheduling/appointments",
        json={
            "patient_id": "patient-2",
            "professional_id": "professional-2",
            "scheduled_at": "20-03-2026 10:30",
            "reason": "Consulta",
        },
        headers=AUTH_HEADER,
    )
    assert response.status_code == 400
    assert "ISO-8601" in response.json()["detail"]


def test_delete_requires_admin_role(monkeypatch):
    _auth_ok(monkeypatch)
    created = client.post(
        "/api/v1/scheduling/appointments",
        json={
            "patient_id": "patient-3",
            "professional_id": "professional-3",
            "scheduled_at": "2026-03-21T09:00:00Z",
            "reason": "Primeira consulta",
        },
        headers=AUTH_HEADER,
    ).json()

    _auth_ok(monkeypatch, allowed_roles={"profissional"})
    forbidden = client.delete(
        f"/api/v1/scheduling/appointments/{created['id']}",
        headers=AUTH_HEADER,
    )
    assert forbidden.status_code == 403


def test_protected_endpoints_reject_invalid_token(monkeypatch):
    _auth_invalid(monkeypatch)

    response = client.get("/api/v1/scheduling/appointments", headers=AUTH_HEADER)
    assert response.status_code == 401
