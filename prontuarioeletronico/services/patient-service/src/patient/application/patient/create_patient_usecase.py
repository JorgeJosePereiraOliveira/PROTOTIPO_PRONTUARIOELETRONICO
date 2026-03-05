from dataclasses import dataclass
from uuid import uuid4

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.patient.patient_entity import Patient
from ...domain.patient.patient_repository_interface import PatientRepositoryInterface


@dataclass
class CreatePatientInputDTO:
    name: str
    cpf: str
    date_of_birth: str
    gender: str


@dataclass
class CreatePatientOutputDTO:
    id: str
    name: str
    cpf: str
    date_of_birth: str
    gender: str


class CreatePatientUseCase(UseCase[CreatePatientInputDTO, CreatePatientOutputDTO]):
    def __init__(self, repository: PatientRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: CreatePatientInputDTO) -> CreatePatientOutputDTO:
        name = input_dto.name.strip()
        cpf = input_dto.cpf.strip()
        date_of_birth = input_dto.date_of_birth.strip()
        gender = input_dto.gender.strip().upper()

        if len(name) < 3:
            raise ValueError("name must have at least 3 characters")
        if not cpf.isdigit() or len(cpf) != 11:
            raise ValueError("cpf must contain 11 numeric digits")
        if gender not in {"M", "F", "O", "N"}:
            raise ValueError("gender must be one of: M, F, O, N")

        existing = self._repository.find_by_cpf(cpf)
        if existing is not None:
            raise ValueError("cpf already registered")

        entity = Patient(
            id=str(uuid4()),
            name=name,
            cpf=cpf,
            date_of_birth=date_of_birth,
            gender=gender,
        )
        self._repository.add(entity)

        return CreatePatientOutputDTO(
            id=entity.id,
            name=entity.name,
            cpf=entity.cpf,
            date_of_birth=entity.date_of_birth,
            gender=entity.gender,
        )