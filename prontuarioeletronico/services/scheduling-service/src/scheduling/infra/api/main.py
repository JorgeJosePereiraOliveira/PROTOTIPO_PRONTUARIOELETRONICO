from dataclasses import asdict
import os

from fastapi import Depends, FastAPI, Header, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict

from ...application.scheduling.create_appointment_usecase import (
    CreateAppointmentInputDTO,
    CreateAppointmentUseCase,
)
from ...application.scheduling.delete_appointment_usecase import (
    DeleteAppointmentInputDTO,
    DeleteAppointmentUseCase,
)
from ...application.scheduling.find_appointment_usecase import (
    FindAppointmentInputDTO,
    FindAppointmentUseCase,
)
from ...application.scheduling.list_appointments_usecase import ListAppointmentsUseCase
from ...infra.auth.auth_service_client import AuthServiceClient
from ...infra.scheduling.database import SessionLocal, init_database
from ...infra.scheduling.sqlalchemy_appointment_repository import (
    SqlAlchemyAppointmentRepository,
)


app = FastAPI(
    title="Scheduling Service",
    version="1.0.0",
    description="Microsserviço de agendamento em Clean Architecture (MS-04)",
)


APP_ENV = os.getenv("APP_ENV", "development")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
if AUTH_SERVICE_URL is None:
    if APP_ENV in {"production", "staging"}:
        raise RuntimeError("AUTH_SERVICE_URL is required for production/staging")
    AUTH_SERVICE_URL = "http://localhost:8001"


class CreateAppointmentRequest(BaseModel):
    patient_id: str
    professional_id: str
    scheduled_at: str
    reason: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "patient_id": "patient-123",
                "professional_id": "professional-456",
                "scheduled_at": "2026-03-15T14:30:00Z",
                "reason": "Retorno clinico de rotina",
            }
        }
    )


init_database()
_db_session = SessionLocal()
_repository = SqlAlchemyAppointmentRepository(_db_session)
_create_appointment_usecase = CreateAppointmentUseCase(_repository)
_find_appointment_usecase = FindAppointmentUseCase(_repository)
_list_appointments_usecase = ListAppointmentsUseCase(_repository)
_delete_appointment_usecase = DeleteAppointmentUseCase(_repository)
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
    return {"status": "healthy", "service": "scheduling"}


@app.get("/api/v1/info")
def service_info():
    return {
        "service": "scheduling",
        "architecture": "clean-architecture",
        "layers": ["domain", "application", "infra"],
    }


@app.post("/api/v1/scheduling/appointments", status_code=201)
def create_appointment(
    payload: CreateAppointmentRequest,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    try:
        output = _create_appointment_usecase.execute(
            CreateAppointmentInputDTO(
                patient_id=payload.patient_id,
                professional_id=payload.professional_id,
                scheduled_at=payload.scheduled_at,
                reason=payload.reason,
            )
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return asdict(output)


@app.get("/api/v1/scheduling/appointments/{appointment_id}")
def get_appointment(
    appointment_id: str,
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    output = _find_appointment_usecase.execute(FindAppointmentInputDTO(id=appointment_id))
    if output is None:
        raise HTTPException(status_code=404, detail="appointment not found")

    return asdict(output)


@app.get("/api/v1/scheduling/appointments")
def list_appointments(
    _auth: dict = Depends(_require_roles(["admin", "profissional"])),
):
    output = _list_appointments_usecase.execute(None)
    return [asdict(item) for item in output.appointments]


@app.delete("/api/v1/scheduling/appointments/{appointment_id}")
def delete_appointment(
    appointment_id: str,
    _auth: dict = Depends(_require_roles(["admin"])),
):
    output = _delete_appointment_usecase.execute(DeleteAppointmentInputDTO(id=appointment_id))
    if not output.deleted:
        raise HTTPException(status_code=404, detail="appointment not found")

    return {"deleted": True}


def _reset_for_tests() -> None:
    _repository.clear()
