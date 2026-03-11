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
    captured_events: list[tuple[str, dict]] = []

    def create_event(token: str, payload: dict) -> dict:
        captured_events.append((token, payload))
        return {"id": "event-1"}

    monkeypatch.setattr(main._audit_client, "create_event", create_event)

    create_response = client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-100",
            "description": "Diabetes mellitus tipo 2",
            "terminology_system": "cid",
            "terminology_code": "E11",
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
    assert get_response.json()["terminology_system"] == "cid"
    assert get_response.json()["terminology_code"] == "E11"
    assert len(captured_events) == 1
    token, payload = captured_events[0]
    assert token == "fake-token"
    assert payload["operation"] == "validate_terminology_code"
    assert payload["status"] == "success"
    assert payload["resource_type"] == "problem"
    assert payload["metadata"]["terminology_system"] == "cid"
    assert payload["metadata"]["terminology_code"] == "E11"


def test_create_soap_and_find_soap(monkeypatch):
    _auth_ok(monkeypatch)

    problem = client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-101",
            "description": "Asma persistente",
            "terminology_system": "cid",
            "terminology_code": "J45.9",
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


def test_timeline_returns_problem_and_soap_events(monkeypatch):
    _auth_ok(monkeypatch)

    problem = client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-timeline-1",
            "description": "Hipertensao em acompanhamento",
            "terminology_system": "cid",
            "terminology_code": "I10",
            "status": "active",
        },
        headers=AUTH_HEADER,
    ).json()

    soap = client.post(
        "/api/v1/emr/soap",
        json={
            "problem_id": problem["id"],
            "patient_id": "patient-timeline-1",
            "professional_id": "prof-timeline-1",
            "subjective": "Paciente refere elevacao pressorica noturna frequente.",
            "objective": "PA aferida em 150x95 mmHg na consulta.",
            "assessment": "Hipertensao arterial sem lesao de orgao-alvo aparente.",
            "plan": "Ajustar terapia e retorno em 14 dias para reavaliacao.",
        },
        headers=AUTH_HEADER,
    ).json()

    response = client.get(
        "/api/v1/emr/timeline",
        params={"patient_id": "patient-timeline-1", "problem_id": problem["id"]},
        headers=AUTH_HEADER,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["patient_id"] == "patient-timeline-1"
    assert payload["problem_id"] == problem["id"]
    assert len(payload["events"]) == 2
    assert payload["events"][0]["event_type"] == "problem"
    assert payload["events"][1]["event_type"] == "soap"
    assert payload["events"][1]["event_id"] == soap["id"]


def test_timeline_rejects_unknown_problem(monkeypatch):
    _auth_ok(monkeypatch)

    response = client.get(
        "/api/v1/emr/timeline",
        params={"patient_id": "patient-timeline-2", "problem_id": "problem-inexistente"},
        headers=AUTH_HEADER,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "problem not found"


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


def test_create_soap_rejects_short_clinical_sections(monkeypatch):
    _auth_ok(monkeypatch)

    problem = client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-201",
            "description": "Dor cronica em ombro direito",
            "terminology_system": "ciap",
            "terminology_code": "R05",
            "status": "active",
        },
        headers=AUTH_HEADER,
    ).json()

    response = client.post(
        "/api/v1/emr/soap",
        json={
            "problem_id": problem["id"],
            "patient_id": "patient-201",
            "professional_id": "prof-03",
            "subjective": "Dor",
            "objective": "PA 120x80",
            "assessment": "Quadro leve",
            "plan": "Reavaliar",
        },
        headers=AUTH_HEADER,
    )

    assert response.status_code == 400
    assert "subjective must have at least 10 characters" in response.json()["detail"]


def test_create_soap_rejects_placeholder_values(monkeypatch):
    _auth_ok(monkeypatch)

    problem = client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-202",
            "description": "Cefaleia tensional recorrente",
            "terminology_system": "ciap",
            "terminology_code": "K86",
            "status": "active",
        },
        headers=AUTH_HEADER,
    ).json()

    response = client.post(
        "/api/v1/emr/soap",
        json={
            "problem_id": problem["id"],
            "patient_id": "patient-202",
            "professional_id": "prof-04",
            "subjective": "sem dados",
            "objective": "Exame fisico dentro da normalidade.",
            "assessment": "Cefaleia primaria sem sinais de alarme.",
            "plan": "Orientacoes gerais e analgesico se necessario.",
        },
        headers=AUTH_HEADER,
    )

    assert response.status_code == 400
    assert "subjective cannot use placeholder values" in response.json()["detail"]


def test_create_soap_rejects_identical_assessment_and_plan(monkeypatch):
    _auth_ok(monkeypatch)

    problem = client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-203",
            "description": "Lombalgia mecanica",
            "terminology_system": "ciap",
            "terminology_code": "T90",
            "status": "active",
        },
        headers=AUTH_HEADER,
    ).json()

    same_text = "Melhorar higiene do sono e manter atividade fisica regular."

    response = client.post(
        "/api/v1/emr/soap",
        json={
            "problem_id": problem["id"],
            "patient_id": "patient-203",
            "professional_id": "prof-05",
            "subjective": "Paciente relata dor lombar ao final do dia de trabalho.",
            "objective": "Sem deficit neurologico focal ao exame fisico.",
            "assessment": same_text,
            "plan": same_text,
        },
        headers=AUTH_HEADER,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "assessment and plan must not be identical"


def test_create_soap_rejects_identical_subjective_and_objective(monkeypatch):
    _auth_ok(monkeypatch)

    problem = client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-204",
            "description": "Cefaleia persistente",
            "terminology_system": "ciap",
            "terminology_code": "R05",
            "status": "active",
        },
        headers=AUTH_HEADER,
    ).json()

    same_text = "Paciente relata dor frontal de forte intensidade ha 2 dias."

    response = client.post(
        "/api/v1/emr/soap",
        json={
            "problem_id": problem["id"],
            "patient_id": "patient-204",
            "professional_id": "prof-06",
            "subjective": same_text,
            "objective": same_text,
            "assessment": "Cefaleia sem sinais de alarme no momento.",
            "plan": "Analgesia, hidratacao e reavaliacao em 48 horas.",
        },
        headers=AUTH_HEADER,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "subjective and objective must not be identical"


def test_protected_endpoints_reject_invalid_token(monkeypatch):
    _auth_invalid(monkeypatch)

    response = client.get("/api/v1/emr/problems/problem-1", headers=AUTH_HEADER)
    assert response.status_code == 401


def test_validate_terminology_code_success(monkeypatch):
    _auth_ok(monkeypatch)

    response = client.get(
        "/api/v1/emr/terminology/validate",
        params={"system": "cid", "code": "J45.9"},
        headers=AUTH_HEADER,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is True
    assert body["system"] == "cid"
    assert body["code"] == "J45.9"


def test_validate_terminology_code_rejects_invalid_format(monkeypatch):
    _auth_ok(monkeypatch)

    response = client.get(
        "/api/v1/emr/terminology/validate",
        params={"system": "ciap", "code": "123"},
        headers=AUTH_HEADER,
    )
    assert response.status_code == 400
    assert "code format is invalid" in response.json()["detail"]


def test_validate_terminology_code_rejects_unknown_code(monkeypatch):
    _auth_ok(monkeypatch)

    response = client.get(
        "/api/v1/emr/terminology/validate",
        params={"system": "sigtap", "code": "9999999999"},
        headers=AUTH_HEADER,
    )
    assert response.status_code == 400
    assert "code not found or inactive" in response.json()["detail"]


def test_create_problem_rejects_invalid_terminology_code(monkeypatch):
    _auth_ok(monkeypatch)
    captured_events: list[tuple[str, dict]] = []

    def create_event(token: str, payload: dict) -> dict:
        captured_events.append((token, payload))
        return {"id": "event-2"}

    monkeypatch.setattr(main._audit_client, "create_event", create_event)

    response = client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-205",
            "description": "Asma em acompanhamento",
            "terminology_system": "cid",
            "terminology_code": "INVALID",
            "status": "active",
        },
        headers=AUTH_HEADER,
    )

    assert response.status_code == 400
    assert "code format is invalid" in response.json()["detail"]
    assert len(main._problem_repository.find_all()) == 0
    assert len(captured_events) == 1
    token, payload = captured_events[0]
    assert token == "fake-token"
    assert payload["status"] == "failed"
    assert payload["resource_id"] == "pending"
    assert payload["metadata"]["validation_error"].startswith("code format is invalid")


def test_protected_endpoints_reject_insufficient_role(monkeypatch):
    _auth_ok(monkeypatch, allowed_roles={"recepcao"})

    response = client.post(
        "/api/v1/emr/problems",
        json={
            "patient_id": "patient-300",
            "description": "Enxaqueca cronica",
            "terminology_system": "cid",
            "terminology_code": "I10",
            "status": "active",
        },
        headers=AUTH_HEADER,
    )
    assert response.status_code == 403
