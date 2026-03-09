from dataclasses import dataclass
from uuid import uuid4

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.emr.problem_entity import Problem
from ...domain.emr.problem_repository_interface import ProblemRepositoryInterface


@dataclass
class CreateProblemInputDTO:
    patient_id: str
    description: str
    status: str = "active"


@dataclass
class CreateProblemOutputDTO:
    id: str
    patient_id: str
    description: str
    status: str


class CreateProblemUseCase(UseCase[CreateProblemInputDTO, CreateProblemOutputDTO]):
    def __init__(self, repository: ProblemRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: CreateProblemInputDTO) -> CreateProblemOutputDTO:
        patient_id = input_dto.patient_id.strip()
        description = input_dto.description.strip()
        status = input_dto.status.strip().lower()

        if not patient_id:
            raise ValueError("patient_id is required")
        if len(description) < 3:
            raise ValueError("description must have at least 3 characters")
        if status not in {"active", "resolved", "inactive"}:
            raise ValueError("status must be one of: active, resolved, inactive")

        entity = Problem(
            id=str(uuid4()),
            patient_id=patient_id,
            description=description,
            status=status,
        )
        self._repository.add(entity)

        return CreateProblemOutputDTO(
            id=entity.id,
            patient_id=entity.patient_id,
            description=entity.description,
            status=entity.status,
        )
