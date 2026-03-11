from dataclasses import dataclass
from uuid import uuid4

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.emr.problem_entity import Problem
from ...domain.emr.problem_repository_interface import ProblemRepositoryInterface
from .validate_terminology_code_usecase import (
    ValidateTerminologyCodeInputDTO,
    ValidateTerminologyCodeUseCase,
)


@dataclass
class CreateProblemInputDTO:
    patient_id: str
    description: str
    terminology_system: str
    terminology_code: str
    status: str = "active"


@dataclass
class CreateProblemOutputDTO:
    id: str
    patient_id: str
    description: str
    terminology_system: str
    terminology_code: str
    status: str
    created_at: str


class CreateProblemUseCase(UseCase[CreateProblemInputDTO, CreateProblemOutputDTO]):
    def __init__(
        self,
        repository: ProblemRepositoryInterface,
        terminology_validator: ValidateTerminologyCodeUseCase | None = None,
    ):
        self._repository = repository
        self._terminology_validator = terminology_validator or ValidateTerminologyCodeUseCase()

    def execute(self, input_dto: CreateProblemInputDTO) -> CreateProblemOutputDTO:
        patient_id = input_dto.patient_id.strip()
        description = input_dto.description.strip()
        terminology_system = input_dto.terminology_system.strip().lower()
        terminology_code = input_dto.terminology_code.strip().upper()
        status = input_dto.status.strip().lower()

        if not patient_id:
            raise ValueError("patient_id is required")
        if len(description) < 3:
            raise ValueError("description must have at least 3 characters")
        if status not in {"active", "resolved", "inactive"}:
            raise ValueError("status must be one of: active, resolved, inactive")

        self._terminology_validator.execute(
            ValidateTerminologyCodeInputDTO(
                system=terminology_system,
                code=terminology_code,
            )
        )

        entity = Problem(
            id=str(uuid4()),
            patient_id=patient_id,
            description=description,
            terminology_system=terminology_system,
            terminology_code=terminology_code,
            status=status,
        )
        self._repository.add(entity)

        return CreateProblemOutputDTO(
            id=entity.id,
            patient_id=entity.patient_id,
            description=entity.description,
            terminology_system=entity.terminology_system,
            terminology_code=entity.terminology_code,
            status=entity.status,
            created_at=entity.created_at,
        )
