from dataclasses import asdict
from datetime import datetime, timezone
import os

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict

from ...application.professional.activate_professional_usecase import (
    ActivateProfessionalInputDTO,
    ActivateProfessionalUseCase,
)
from ...application.professional.deactivate_professional_usecase import (
    DeactivateProfessionalInputDTO,
    DeactivateProfessionalUseCase,
)
from ...application.professional.find_professional_usecase import (
    FindProfessionalInputDTO,
    FindProfessionalUseCase,
)
from ...application.professional.list_professionals_usecase import (
    ListProfessionalsInputDTO,
    ListProfessionalsUseCase,
)
from ...application.professional.register_professional_usecase import (
    RegisterProfessionalInputDTO,
    RegisterProfessionalUseCase,
)
from ...infra.audit.audit_service_client import AuditServiceClient
from ...infra.auth.auth_service_client import AuthServiceClient
from ...infra.professional.database import SessionLocal, init_database
from ...infra.professional.sqlalchemy_professional_repository import (
    SqlAlchemyProfessionalRepository,
)


app = FastAPI(
    title="Professional Service",
    version="1.0.0",
    description="Microsservico de profissionais em Clean Architecture (MS-06)",
)


APP_ENV = os.getenv("APP_ENV", "development")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
AUDIT_SERVICE_URL = os.getenv("AUDIT_SERVICE_URL")
if AUTH_SERVICE_URL is None:
    if APP_ENV in {"production", "staging"}:
        raise RuntimeError("AUTH_SERVICE_URL is required for production/staging")
    AUTH_SERVICE_URL = "http://localhost:8001"
if AUDIT_SERVICE_URL is None:
    if APP_ENV in {"production", "staging"}:
        raise RuntimeError("AUDIT_SERVICE_URL is required for production/staging")
    AUDIT_SERVICE_URL = "http://localhost:8005"


class CreateProfessionalRequest(BaseModel):
    full_name: str
    document_cpf: str
    council_type: str
    council_uf: str
    council_number: str
    occupation: str
    specialty: str | None = None
    auth_user_id: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "Dra. Ana Paula Souza",
                "document_cpf": "12345678901",
                "council_type": "CRM",
                "council_uf": "SP",
                "council_number": "123456",
                "occupation": "medico",
                "specialty": "clinica medica",
                "auth_user_id": "user-123",
            }
        }
    )


init_database()
_db_session = SessionLocal()
_repository = SqlAlchemyProfessionalRepository(_db_session)
_register_usecase = RegisterProfessionalUseCase(_repository)
_find_usecase = FindProfessionalUseCase(_repository)
_list_usecase = ListProfessionalsUseCase(_repository)
_activate_usecase = ActivateProfessionalUseCase(_repository)
_deactivate_usecase = DeactivateProfessionalUseCase(_repository)
_auth_client = AuthServiceClient(base_url=AUTH_SERVICE_URL)
_audit_client = AuditServiceClient(base_url=AUDIT_SERVICE_URL)
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


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _emit_professional_audit_event(
    token: str,
    verified_claims: dict,
    operation: str,
    status: str,
    resource_id: str,
    metadata: dict,
) -> None:
    claims = verified_claims.get("claims", {})
    actor_id = str(claims.get("sub") or claims.get("username") or "unknown")
    actor_role = str(claims.get("role") or "unknown")

    try:
        _audit_client.create_event(
            token=token,
            payload={
                "actor_id": actor_id,
                "actor_role": actor_role,
                "context": "professional",
                "operation": operation,
                "resource_type": "professional",
                "resource_id": resource_id,
                "status": status,
                "occurred_at": _iso_utc_now(),
                "metadata": metadata,
            },
        )
    except ValueError:
        return


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "professional"}


@app.get("/api/v1/info")
def service_info():
    return {
        "service": "professional",
        "architecture": "clean-architecture",
        "layers": ["domain", "application", "infra"],
    }


@app.post("/api/v1/professionals", status_code=201)
def create_professional(
    payload: CreateProfessionalRequest,
    _auth: dict = Depends(_require_roles(["admin"])),
    authorization: str | None = Header(default=None),
):
    token = _extract_bearer_token(authorization)

    try:
        output = _register_usecase.execute(
            RegisterProfessionalInputDTO(
                full_name=payload.full_name,
                document_cpf=payload.document_cpf,
                council_type=payload.council_type,
                council_uf=payload.council_uf,
                council_number=payload.council_number,
                occupation=payload.occupation,
                specialty=payload.specialty,
                auth_user_id=payload.auth_user_id,
            )
        )
    except ValueError as error:
        detail = str(error)
        _emit_professional_audit_event(
            token=token,
            verified_claims=_auth,
            operation="create_professional",
            status="failed",
            resource_id="pending",
            metadata={
                "council_type": payload.council_type,
                "council_uf": payload.council_uf,
                "council_number": payload.council_number,
                "error": detail,
            },
        )
        raise HTTPException(status_code=400, detail=detail) from error

    _emit_professional_audit_event(
        token=token,
        verified_claims=_auth,
        operation="create_professional",
        status="success",
        resource_id=output.id,
        metadata={
            "council_type": output.council_type,
            "council_uf": output.council_uf,
            "council_number": output.council_number,
            "status": output.status,
        },
    )

    return asdict(output)


@app.get("/api/v1/professionals/{professional_id}")
def get_professional(
    professional_id: str,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    output = _find_usecase.execute(FindProfessionalInputDTO(id=professional_id))
    if output is None:
        raise HTTPException(status_code=404, detail="professional not found")

    return asdict(output)


@app.get("/api/v1/professionals")
def list_professionals(
    council_type: str | None = Query(default=None),
    council_uf: str | None = Query(default=None),
    council_number: str | None = Query(default=None),
    status: str | None = Query(default=None),
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    try:
        output = _list_usecase.execute(
            ListProfessionalsInputDTO(
                council_type=council_type,
                council_uf=council_uf,
                council_number=council_number,
                status=status,
            )
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return [asdict(item) for item in output.professionals]


@app.post("/api/v1/professionals/{professional_id}/activate")
def activate_professional(
    professional_id: str,
    _auth: dict = Depends(_require_roles(["admin"])),
    authorization: str | None = Header(default=None),
):
    token = _extract_bearer_token(authorization)

    try:
        output = _activate_usecase.execute(ActivateProfessionalInputDTO(id=professional_id))
    except ValueError as error:
        detail = str(error)
        _emit_professional_audit_event(
            token=token,
            verified_claims=_auth,
            operation="activate_professional",
            status="failed",
            resource_id=professional_id,
            metadata={"error": detail},
        )
        if detail == "professional not found":
            raise HTTPException(status_code=404, detail=detail) from error
        raise HTTPException(status_code=400, detail=detail) from error

    _emit_professional_audit_event(
        token=token,
        verified_claims=_auth,
        operation="activate_professional",
        status="success",
        resource_id=output.id,
        metadata={"status": output.status, "updated_at": output.updated_at},
    )

    return asdict(output)


@app.post("/api/v1/professionals/{professional_id}/deactivate")
def deactivate_professional(
    professional_id: str,
    _auth: dict = Depends(_require_roles(["admin"])),
    authorization: str | None = Header(default=None),
):
    token = _extract_bearer_token(authorization)

    try:
        output = _deactivate_usecase.execute(
            DeactivateProfessionalInputDTO(id=professional_id)
        )
    except ValueError as error:
        detail = str(error)
        _emit_professional_audit_event(
            token=token,
            verified_claims=_auth,
            operation="deactivate_professional",
            status="failed",
            resource_id=professional_id,
            metadata={"error": detail},
        )
        if detail == "professional not found":
            raise HTTPException(status_code=404, detail=detail) from error
        raise HTTPException(status_code=400, detail=detail) from error

    _emit_professional_audit_event(
        token=token,
        verified_claims=_auth,
        operation="deactivate_professional",
        status="success",
        resource_id=output.id,
        metadata={"status": output.status, "updated_at": output.updated_at},
    )

    return asdict(output)


def _reset_for_tests() -> None:
    _db_session.rollback()
    _repository.clear()
