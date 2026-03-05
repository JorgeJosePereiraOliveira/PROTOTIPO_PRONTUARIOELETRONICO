from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.patient.patient_repository_interface import PatientRepositoryInterface


@dataclass
class PatientListItemDTO:
    id: str
    name: str
    cpf: str
    date_of_birth: str
    gender: str


@dataclass
class ListPatientsOutputDTO:
    patients: list[PatientListItemDTO]


class ListPatientsUseCase(UseCase[None, ListPatientsOutputDTO]):
    def __init__(self, repository: PatientRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: None) -> ListPatientsOutputDTO:
        entities = self._repository.find_all()
        return ListPatientsOutputDTO(
            patients=[
                PatientListItemDTO(
                    id=item.id,
                    name=item.name,
                    cpf=item.cpf,
                    date_of_birth=item.date_of_birth,
                    gender=item.gender,
                )
                for item in entities
            ]
        )