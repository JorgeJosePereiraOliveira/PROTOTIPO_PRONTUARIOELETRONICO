from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.patient.patient_repository_interface import PatientRepositoryInterface


@dataclass
class DeletePatientInputDTO:
    id: str


@dataclass
class DeletePatientOutputDTO:
    deleted: bool


class DeletePatientUseCase(UseCase[DeletePatientInputDTO, DeletePatientOutputDTO]):
    def __init__(self, repository: PatientRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: DeletePatientInputDTO) -> DeletePatientOutputDTO:
        entity = self._repository.find_by_id(input_dto.id)
        if entity is None:
            return DeletePatientOutputDTO(deleted=False)

        self._repository.delete(input_dto.id)
        return DeletePatientOutputDTO(deleted=True)