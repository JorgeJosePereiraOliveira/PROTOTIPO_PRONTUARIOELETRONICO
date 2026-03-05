from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.patient.patient_repository_interface import PatientRepositoryInterface


@dataclass
class FindPatientInputDTO:
    id: str


@dataclass
class FindPatientOutputDTO:
    id: str
    name: str
    cpf: str
    date_of_birth: str
    gender: str


class FindPatientUseCase(UseCase[FindPatientInputDTO, FindPatientOutputDTO | None]):
    def __init__(self, repository: PatientRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: FindPatientInputDTO) -> FindPatientOutputDTO | None:
        entity = self._repository.find_by_id(input_dto.id)
        if entity is None:
            return None

        return FindPatientOutputDTO(
            id=entity.id,
            name=entity.name,
            cpf=entity.cpf,
            date_of_birth=entity.date_of_birth,
            gender=entity.gender,
        )