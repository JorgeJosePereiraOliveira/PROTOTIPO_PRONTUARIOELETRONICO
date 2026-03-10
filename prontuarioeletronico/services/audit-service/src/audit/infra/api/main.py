from dataclasses import asdict
import os

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict

from ...application.audit.create_audit_event_usecase import (
    CreateAuditEventInputDTO,
    CreateAuditEventUseCase,
)
from ...application.audit.find_audit_event_usecase import (
    FindAuditEventInputDTO,
    FindAuditEventUseCase,
)
from ...application.audit.list_audit_events_usecase import (
    ListAuditEventsInputDTO,
    ListAuditEventsUseCase,
)
from ...infra.audit.database import SessionLocal, init_database
from ...infra.audit.sqlalchemy_audit_event_repository import SqlAlchemyAuditEventRepository
from ...infra.auth.auth_service_client import AuthServiceClient


app = FastAPI(
    title="Audit Service",
    version="1.0.0",
    description="Microsservico de auditoria em Clean Architecture (MS-05)",
)


APP_ENV = os.getenv("APP_ENV", "development")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
if AUTH_SERVICE_URL is None:
    if APP_ENV in {"production", "staging"}:
        raise RuntimeError("AUTH_SERVICE_URL is required for production/staging")
    AUTH_SERVICE_URL = "http://localhost:8001"


class CreateAuditEventRequest(BaseModel):
    actor_id: str
    actor_role: str
    context: str
    operation: str
    resource_type: str
    resource_id: str
    status: str
    occurred_at: str
    metadata: dict | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "actor_id": "user-123",
                "actor_role": "profissional",
                "context": "emr",
                "operation": "create",
                "resource_type": "soap_record",
                "resource_id": "soap-789",
                "status": "success",
                "occurred_at": "2026-03-10T10:30:00Z",
                "metadata": {"source": "gateway"},
            }
        }
    )


init_database()
_db_session = SessionLocal()
_repository = SqlAlchemyAuditEventRepository(_db_session)
_create_usecase = CreateAuditEventUseCase(_repository)
_find_usecase = FindAuditEventUseCase(_repository)
_list_usecase = ListAuditEventsUseCase(_repository)
_auth_client = AuthServiceClient(base_url=AUTH_SERVICE_URL)
_bearer_scheme = HTTPBearer(auto_error=False)


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="missing authorization header")

    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise HTTPException(status_code=401, detail="invalid authorization scheme")

    token = authorization[len(prefix):].strip()
    if not token:
        raise HTTPException(status_code=401, detail="empty bearer token")
    return token


def _require_roles(required_roles: list[str]):
    def dependency(
        authorization: str | None = Header(default=None),
        bearer: HTTPAuthorizationCredentials | None = Security(_bearer_scheme),
    ) -> dict:
        token = bearer.credentials if bearer else _extract_bearer_token(authorization)

        try:
            verified = _auth_client.verify(token)
        except ValueError as error:
            raise HTTPException(status_code=401, detail=str(error)) from error

        for role in required_roles:
            try:
                if _auth_client.authorize(token, role):
                    return verified
            except ValueError:
                continue

        raise HTTPException(status_code=403, detail="insufficient role")

    return dependency


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "audit"}


@app.get("/api/v1/info")
def service_info():
    return {
        "service": "audit",
        "architecture": "clean-architecture",
        "layers": ["domain", "application", "infra"],
    }


@app.post("/api/v1/audit/events", status_code=201)
def create_audit_event(
    payload: CreateAuditEventRequest,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    try:
        output = _create_usecase.execute(
            CreateAuditEventInputDTO(
                actor_id=payload.actor_id,
                actor_role=payload.actor_role,
                context=payload.context,
                operation=payload.operation,
                resource_type=payload.resource_type,
                resource_id=payload.resource_id,
                status=payload.status,
                occurred_at=payload.occurred_at,
                metadata=payload.metadata,
            )
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return asdict(output)


@app.get("/api/v1/audit/events/{event_id}")
def get_audit_event(
    event_id: str,
    _auth: dict = Depends(_require_roles(["admin"])),
):
    output = _find_usecase.execute(FindAuditEventInputDTO(id=event_id))
    if output is None:
        raise HTTPException(status_code=404, detail="audit event not found")

    return asdict(output)


@app.get("/api/v1/audit/events")
def list_audit_events(
    actor_id: str | None = Query(default=None),
    operation: str | None = Query(default=None),
    from_datetime: str | None = Query(default=None, alias="from"),
    to_datetime: str | None = Query(default=None, alias="to"),
    _auth: dict = Depends(_require_roles(["admin"])),
):
    try:
        output = _list_usecase.execute(
            ListAuditEventsInputDTO(
                actor_id=actor_id,
                operation=operation,
                from_datetime=from_datetime,
                to_datetime=to_datetime,
            )
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return [asdict(item) for item in output.events]


def _reset_for_tests() -> None:
    _repository.clear()
