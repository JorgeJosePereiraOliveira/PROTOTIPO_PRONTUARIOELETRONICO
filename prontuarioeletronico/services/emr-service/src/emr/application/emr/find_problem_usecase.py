from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.emr.problem_repository_interface import ProblemRepositoryInterface


@dataclass
class FindProblemInputDTO:
    id: str


@dataclass
class FindProblemOutputDTO:
    id: str
    patient_id: str
    description: str
    status: str


class FindProblemUseCase(UseCase[FindProblemInputDTO, FindProblemOutputDTO | None]):
    def __init__(self, repository: ProblemRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: FindProblemInputDTO) -> FindProblemOutputDTO | None:
        entity = self._repository.find_by_id(input_dto.id)
        if entity is None:
            return None

        return FindProblemOutputDTO(
            id=entity.id,
            patient_id=entity.patient_id,
            description=entity.description,
            status=entity.status,
        )
