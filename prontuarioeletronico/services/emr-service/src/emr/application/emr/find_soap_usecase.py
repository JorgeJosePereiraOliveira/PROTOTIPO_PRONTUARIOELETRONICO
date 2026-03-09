from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.emr.soap_repository_interface import SOAPRepositoryInterface


@dataclass
class FindSOAPInputDTO:
    id: str


@dataclass
class FindSOAPOutputDTO:
    id: str
    problem_id: str
    patient_id: str
    professional_id: str
    subjective: str
    objective: str
    assessment: str
    plan: str


class FindSOAPUseCase(UseCase[FindSOAPInputDTO, FindSOAPOutputDTO | None]):
    def __init__(self, repository: SOAPRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: FindSOAPInputDTO) -> FindSOAPOutputDTO | None:
        entity = self._repository.find_by_id(input_dto.id)
        if entity is None:
            return None

        return FindSOAPOutputDTO(
            id=entity.id,
            problem_id=entity.problem_id,
            patient_id=entity.patient_id,
            professional_id=entity.professional_id,
            subjective=entity.subjective,
            objective=entity.objective,
            assessment=entity.assessment,
            plan=entity.plan,
        )
