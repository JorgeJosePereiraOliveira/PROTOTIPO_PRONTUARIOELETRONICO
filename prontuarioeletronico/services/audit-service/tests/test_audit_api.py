from fastapi.testclient import TestClient

from src.audit.infra.api import main


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


def test_create_get_list_audit_event(monkeypatch):
    _auth_ok(monkeypatch)

    create_response = client.post(
        "/api/v1/audit/events",
        json={
            "actor_id": "user-1",
            "actor_role": "profissional",
            "context": "emr",
            "operation": "create",
            "resource_type": "soap_record",
            "resource_id": "soap-1",
            "status": "success",
            "occurred_at": "2026-03-10T10:30:00Z",
            "metadata": {"source": "gateway"},
        },
        headers=AUTH_HEADER,
    )
    assert create_response.status_code == 201
    event_id = create_response.json()["id"]

    get_response = client.get(
        f"/api/v1/audit/events/{event_id}",
        headers=AUTH_HEADER,
    )
    assert get_response.status_code == 200
    assert get_response.json()["resource_id"] == "soap-1"

    list_response = client.get(
        "/api/v1/audit/events",
        params={"actor_id": "user-1", "operation": "create"},
        headers=AUTH_HEADER,
    )
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_create_audit_event_rejects_invalid_status(monkeypatch):
    _auth_ok(monkeypatch)

    response = client.post(
        "/api/v1/audit/events",
        json={
            "actor_id": "user-2",
            "actor_role": "profissional",
            "context": "patient",
            "operation": "delete",
            "resource_type": "patient",
            "resource_id": "patient-1",
            "status": "ok",
            "occurred_at": "2026-03-10T10:31:00Z",
        },
        headers=AUTH_HEADER,
    )
    assert response.status_code == 400
    assert "status must be one of" in response.json()["detail"]


def test_list_audit_events_rejects_invalid_from(monkeypatch):
    _auth_ok(monkeypatch)

    response = client.get(
        "/api/v1/audit/events",
        params={"from": "2026/03/10 10:31"},
        headers=AUTH_HEADER,
    )
    assert response.status_code == 400
    assert "from must be a valid ISO-8601 datetime" in response.json()["detail"]


def test_read_endpoints_require_admin_role(monkeypatch):
    _auth_ok(monkeypatch, allowed_roles={"profissional"})

    response = client.get("/api/v1/audit/events", headers=AUTH_HEADER)
    assert response.status_code == 403


def test_protected_endpoints_reject_invalid_token(monkeypatch):
    _auth_invalid(monkeypatch)

    response = client.get("/api/v1/audit/events", headers=AUTH_HEADER)
    assert response.status_code == 401
