from dataclasses import asdict
import os

from fastapi import Depends, FastAPI, Header, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict

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
from ...infra.auth.auth_service_client import AuthServiceClient
from ...infra.patient.in_memory_patient_repository import InMemoryPatientRepository


app = FastAPI(
    title="Patient Service",
    version="1.0.0",
    description="Microsserviço de pacientes em Clean Architecture (MS-02)",
)


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


_repository = InMemoryPatientRepository()
_create_patient_usecase = CreatePatientUseCase(_repository)
_find_patient_usecase = FindPatientUseCase(_repository)
_list_patients_usecase = ListPatientsUseCase(_repository)
_update_patient_usecase = UpdatePatientUseCase(_repository)
_delete_patient_usecase = DeletePatientUseCase(_repository)
_auth_client = AuthServiceClient(
    base_url=os.getenv("AUTH_SERVICE_URL", "http://localhost:8001"),
)
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


def _reset_for_tests() -> None:
    _repository.clear()
