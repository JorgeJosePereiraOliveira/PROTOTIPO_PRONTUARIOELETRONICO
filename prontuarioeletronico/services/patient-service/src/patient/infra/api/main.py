from dataclasses import asdict

from fastapi import FastAPI, HTTPException
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


_repository = InMemoryPatientRepository()
_create_patient_usecase = CreatePatientUseCase(_repository)
_find_patient_usecase = FindPatientUseCase(_repository)
_list_patients_usecase = ListPatientsUseCase(_repository)


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
def create_patient(payload: CreatePatientRequest):
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
def get_patient(patient_id: str):
    output = _find_patient_usecase.execute(FindPatientInputDTO(id=patient_id))
    if output is None:
        raise HTTPException(status_code=404, detail="patient not found")

    return asdict(output)


@app.get("/api/v1/patients")
def list_patients():
    output = _list_patients_usecase.execute(None)
    return [asdict(item) for item in output.patients]


def _reset_for_tests() -> None:
    _repository.clear()
