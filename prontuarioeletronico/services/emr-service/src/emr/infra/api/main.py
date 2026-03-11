from dataclasses import asdict
from datetime import datetime, timezone
import os

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict

from ...application.emr.create_problem_usecase import (
    CreateProblemInputDTO,
    CreateProblemUseCase,
)
from ...application.emr.create_soap_usecase import CreateSOAPInputDTO, CreateSOAPUseCase
from ...application.emr.find_problem_usecase import FindProblemInputDTO, FindProblemUseCase
from ...application.emr.find_soap_usecase import FindSOAPInputDTO, FindSOAPUseCase
from ...application.emr.validate_terminology_code_usecase import (
    ValidateTerminologyCodeInputDTO,
    ValidateTerminologyCodeUseCase,
)
from ...infra.audit.audit_service_client import AuditServiceClient
from ...infra.auth.auth_service_client import AuthServiceClient
from ...infra.emr.database import SessionLocal, init_database
from ...infra.emr.sqlalchemy_problem_repository import SqlAlchemyProblemRepository
from ...infra.emr.sqlalchemy_soap_repository import SqlAlchemySOAPRepository


app = FastAPI(
    title="Emr Service",
    version="1.0.0",
    description="Microsserviço EMR RCOP/SOAP em Clean Architecture (MS-03)",
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


class CreateProblemRequest(BaseModel):
    patient_id: str
    description: str
    terminology_system: str
    terminology_code: str
    status: str = "active"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "patient_id": "patient-123",
                "description": "Hipertensao arterial sistemica",
                "terminology_system": "cid",
                "terminology_code": "I10",
                "status": "active",
            }
        }
    )


class CreateSOAPRequest(BaseModel):
    problem_id: str
    patient_id: str
    professional_id: str
    subjective: str
    objective: str
    assessment: str
    plan: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "problem_id": "problem-123",
                "patient_id": "patient-123",
                "professional_id": "professional-456",
                "subjective": "Paciente refere cefaleia intensa ha 3 dias.",
                "objective": "PA aferida em 160x100 mmHg.",
                "assessment": "Hipertensao arterial estagio 2 descompensada.",
                "plan": "Iniciar anti-hipertensivo e retorno em 7 dias.",
            }
        }
    )


init_database()
_db_session = SessionLocal()
_problem_repository = SqlAlchemyProblemRepository(_db_session)
_soap_repository = SqlAlchemySOAPRepository(_db_session)
_validate_terminology_code_usecase = ValidateTerminologyCodeUseCase()
_create_problem_usecase = CreateProblemUseCase(
    _problem_repository,
    terminology_validator=_validate_terminology_code_usecase,
)
_find_problem_usecase = FindProblemUseCase(_problem_repository)
_create_soap_usecase = CreateSOAPUseCase(_soap_repository, _problem_repository)
_find_soap_usecase = FindSOAPUseCase(_soap_repository)
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


def _emit_terminology_audit_event(
    token: str,
    verified_claims: dict,
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
                "context": "emr",
                "operation": "validate_terminology_code",
                "resource_type": "problem",
                "resource_id": resource_id,
                "status": status,
                "occurred_at": _iso_utc_now(),
                "metadata": metadata,
            },
        )
    except ValueError:
        # Audit logging must not block clinical workflow.
        return


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "emr"}


@app.get("/api/v1/info")
def service_info():
    return {
        "service": "emr",
        "architecture": "clean-architecture",
        "layers": ["domain", "application", "infra"],
    }


@app.post("/api/v1/emr/problems", status_code=201)
def create_problem(
    payload: CreateProblemRequest,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
    authorization: str | None = Header(default=None),
):
    token = _extract_bearer_token(authorization)

    try:
        output = _create_problem_usecase.execute(
            CreateProblemInputDTO(
                patient_id=payload.patient_id,
                description=payload.description,
                terminology_system=payload.terminology_system,
                terminology_code=payload.terminology_code,
                status=payload.status,
            )
        )
    except ValueError as error:
        _emit_terminology_audit_event(
            token=token,
            verified_claims=_auth,
            status="failed",
            resource_id="pending",
            metadata={
                "patient_id": payload.patient_id,
                "terminology_system": payload.terminology_system,
                "terminology_code": payload.terminology_code,
                "validation_error": str(error),
            },
        )
        raise HTTPException(status_code=400, detail=str(error)) from error

    _emit_terminology_audit_event(
        token=token,
        verified_claims=_auth,
        status="success",
        resource_id=output.id,
        metadata={
            "patient_id": output.patient_id,
            "terminology_system": output.terminology_system,
            "terminology_code": output.terminology_code,
        },
    )

    return asdict(output)


@app.get("/api/v1/emr/problems/{problem_id}")
def get_problem(
    problem_id: str,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    output = _find_problem_usecase.execute(FindProblemInputDTO(id=problem_id))
    if output is None:
        raise HTTPException(status_code=404, detail="problem not found")

    return asdict(output)


@app.get("/api/v1/emr/terminology/validate")
def validate_terminology_code(
    system: str = Query(...),
    code: str = Query(...),
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    try:
        output = _validate_terminology_code_usecase.execute(
            ValidateTerminologyCodeInputDTO(system=system, code=code)
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return asdict(output)


@app.post("/api/v1/emr/soap", status_code=201)
def create_soap_record(
    payload: CreateSOAPRequest,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    try:
        output = _create_soap_usecase.execute(
            CreateSOAPInputDTO(
                problem_id=payload.problem_id,
                patient_id=payload.patient_id,
                professional_id=payload.professional_id,
                subjective=payload.subjective,
                objective=payload.objective,
                assessment=payload.assessment,
                plan=payload.plan,
            )
        )
    except ValueError as error:
        detail = str(error)
        if detail == "problem not found":
            raise HTTPException(status_code=404, detail=detail) from error
        raise HTTPException(status_code=400, detail=detail) from error

    return asdict(output)


@app.get("/api/v1/emr/soap/{soap_id}")
def get_soap_record(
    soap_id: str,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    output = _find_soap_usecase.execute(FindSOAPInputDTO(id=soap_id))
    if output is None:
        raise HTTPException(status_code=404, detail="soap record not found")

    return asdict(output)


def _reset_for_tests() -> None:
    _db_session.rollback()
    _soap_repository.clear()
    _problem_repository.clear()
