from dataclasses import asdict
from datetime import datetime, timezone
import os

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict

from ...application.consent.create_consent_usecase import (
    CreateConsentInputDTO,
    CreateConsentUseCase,
)
from ...application.consent.list_patient_consents_usecase import (
    ListPatientConsentsInputDTO,
    ListPatientConsentsUseCase,
)
from ...application.consent.revoke_consent_usecase import (
    RevokeConsentInputDTO,
    RevokeConsentUseCase,
)
from ...application.patient.create_patient_usecase import (
    CreatePatientInputDTO,
    CreatePatientUseCase,
)
from ...application.patient.find_patient_usecase import (
    FindPatientInputDTO,
    FindPatientUseCase,
)
from ...application.patient.list_patients_usecase import ListPatientsUseCase
from ...application.patient.update_patient_usecase import (
    UpdatePatientInputDTO,
    UpdatePatientUseCase,
)
from ...application.patient.delete_patient_usecase import (
    DeletePatientInputDTO,
    DeletePatientUseCase,
)
from ...infra.audit.audit_service_client import AuditServiceClient
from ...infra.auth.auth_service_client import AuthServiceClient
from ...infra.patient.database import SessionLocal, init_database
from ...infra.patient.sqlalchemy_consent_repository import SqlAlchemyConsentRepository
from ...infra.patient.sqlalchemy_patient_repository import SqlAlchemyPatientRepository


app = FastAPI(
    title="Patient Service",
    version="1.0.0",
    description="Microsserviço de pacientes em Clean Architecture (MS-02)",
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


class CreatePatientRequest(BaseModel):
    name: str
    cpf: str
    date_of_birth: str
    gender: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Maria da Silva",
                "cpf": "12345678901",
                "date_of_birth": "1990-05-15",
                "gender": "F",
            }
        }
    )


class UpdatePatientRequest(BaseModel):
    name: str
    cpf: str
    date_of_birth: str
    gender: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Maria da Silva Atualizada",
                "cpf": "12345678901",
                "date_of_birth": "1990-05-15",
                "gender": "F",
            }
        }
    )


class CreateConsentRequest(BaseModel):
    legal_basis: str
    purpose: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "legal_basis": "consentimento",
                "purpose": "Compartilhamento de dados clinicos para continuidade do cuidado",
            }
        }
    )


init_database()
_db_session = SessionLocal()
_repository = SqlAlchemyPatientRepository(_db_session)
_consent_repository = SqlAlchemyConsentRepository(_db_session)
_create_patient_usecase = CreatePatientUseCase(_repository)
_find_patient_usecase = FindPatientUseCase(_repository)
_list_patients_usecase = ListPatientsUseCase(_repository)
_update_patient_usecase = UpdatePatientUseCase(_repository)
_delete_patient_usecase = DeletePatientUseCase(_repository)
_create_consent_usecase = CreateConsentUseCase(_consent_repository, _repository)
_list_consents_usecase = ListPatientConsentsUseCase(_consent_repository)
_revoke_consent_usecase = RevokeConsentUseCase(_consent_repository)
_auth_client = AuthServiceClient(
    base_url=AUTH_SERVICE_URL,
)
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


def _emit_consent_audit_event(
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
                "context": "lgpd",
                "operation": operation,
                "resource_type": "patient_consent",
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
    return {"status": "healthy", "service": "patient"}


@app.get("/api/v1/info")
def service_info():
    return {
        "service": "patient",
        "architecture": "clean-architecture",
        "layers": ["domain", "application", "infra"],
    }


@app.post("/api/v1/patients", status_code=201)
def create_patient(
    payload: CreatePatientRequest,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    try:
        output = _create_patient_usecase.execute(
            CreatePatientInputDTO(
                name=payload.name,
                cpf=payload.cpf,
                date_of_birth=payload.date_of_birth,
                gender=payload.gender,
            )
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return asdict(output)


@app.get("/api/v1/patients/{patient_id}")
def get_patient(
    patient_id: str,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    output = _find_patient_usecase.execute(FindPatientInputDTO(id=patient_id))
    if output is None:
        raise HTTPException(status_code=404, detail="patient not found")

    return asdict(output)


@app.get("/api/v1/patients")
def list_patients(_auth: dict = Depends(_require_roles(["admin", "profissional"]))):
    output = _list_patients_usecase.execute(None)
    return [asdict(item) for item in output.patients]


@app.put("/api/v1/patients/{patient_id}")
def update_patient(
    patient_id: str,
    payload: UpdatePatientRequest,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    try:
        output = _update_patient_usecase.execute(
            UpdatePatientInputDTO(
                id=patient_id,
                name=payload.name,
                cpf=payload.cpf,
                date_of_birth=payload.date_of_birth,
                gender=payload.gender,
            )
        )
    except ValueError as error:
        detail = str(error)
        if detail == "patient not found":
            raise HTTPException(status_code=404, detail=detail) from error
        raise HTTPException(status_code=400, detail=detail) from error

    return asdict(output)


@app.delete("/api/v1/patients/{patient_id}")
def delete_patient(
    patient_id: str,
    _auth: dict = Depends(_require_roles(["admin"])),
):
    output = _delete_patient_usecase.execute(DeletePatientInputDTO(id=patient_id))
    if not output.deleted:
        raise HTTPException(status_code=404, detail="patient not found")

    return {"deleted": True}


@app.post("/api/v1/patients/{patient_id}/consents", status_code=201)
def create_consent(
    patient_id: str,
    payload: CreateConsentRequest,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
    authorization: str | None = Header(default=None),
):
    token = _extract_bearer_token(authorization)

    try:
        output = _create_consent_usecase.execute(
            CreateConsentInputDTO(
                patient_id=patient_id,
                legal_basis=payload.legal_basis,
                purpose=payload.purpose,
            )
        )
    except ValueError as error:
        detail = str(error)
        _emit_consent_audit_event(
            token=token,
            verified_claims=_auth,
            operation="create_consent",
            status="failed",
            resource_id="pending",
            metadata={
                "patient_id": patient_id,
                "legal_basis": payload.legal_basis,
                "purpose": payload.purpose,
                "error": detail,
            },
        )
        if detail == "patient not found":
            raise HTTPException(status_code=404, detail=detail) from error
        raise HTTPException(status_code=400, detail=detail) from error

    _emit_consent_audit_event(
        token=token,
        verified_claims=_auth,
        operation="create_consent",
        status="success",
        resource_id=output.id,
        metadata={
            "patient_id": output.patient_id,
            "legal_basis": output.legal_basis,
            "purpose": output.purpose,
            "consent_status": output.status,
        },
    )

    return asdict(output)


@app.get("/api/v1/patients/{patient_id}/consents")
def list_patient_consents(
    patient_id: str,
    status: str | None = Query(default=None),
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    output = _list_consents_usecase.execute(ListPatientConsentsInputDTO(patient_id=patient_id))
    items = [asdict(item) for item in output.consents]
    if status is None:
        return items

    normalized = status.strip().lower()
    if normalized not in {"active", "revoked"}:
        raise HTTPException(status_code=400, detail="status must be one of: active, revoked")
    return [item for item in items if item["status"] == normalized]


@app.post("/api/v1/patients/{patient_id}/consents/{consent_id}/revoke")
def revoke_consent(
    patient_id: str,
    consent_id: str,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
    authorization: str | None = Header(default=None),
):
    token = _extract_bearer_token(authorization)

    try:
        output = _revoke_consent_usecase.execute(
            RevokeConsentInputDTO(patient_id=patient_id, consent_id=consent_id)
        )
    except ValueError as error:
        detail = str(error)
        _emit_consent_audit_event(
            token=token,
            verified_claims=_auth,
            operation="revoke_consent",
            status="failed",
            resource_id=consent_id,
            metadata={"patient_id": patient_id, "error": detail},
        )
        if detail == "consent not found":
            raise HTTPException(status_code=404, detail=detail) from error
        raise HTTPException(status_code=400, detail=detail) from error

    _emit_consent_audit_event(
        token=token,
        verified_claims=_auth,
        operation="revoke_consent",
        status="success",
        resource_id=output.id,
        metadata={
            "patient_id": output.patient_id,
            "consent_status": output.status,
            "revoked_at": output.revoked_at,
        },
    )

    return asdict(output)


def _reset_for_tests() -> None:
    _db_session.rollback()
    _consent_repository.clear()
    _repository.clear()
