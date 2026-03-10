from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.scheduling.appointment_repository_interface import (
    AppointmentRepositoryInterface,
)


@dataclass
class DeleteAppointmentInputDTO:
    id: str


@dataclass
class DeleteAppointmentOutputDTO:
    deleted: bool


class DeleteAppointmentUseCase(
    UseCase[DeleteAppointmentInputDTO, DeleteAppointmentOutputDTO]
):
    def __init__(self, repository: AppointmentRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: DeleteAppointmentInputDTO) -> DeleteAppointmentOutputDTO:
        entity = self._repository.find_by_id(input_dto.id)
        if entity is None:
            return DeleteAppointmentOutputDTO(deleted=False)

        self._repository.delete(input_dto.id)
        return DeleteAppointmentOutputDTO(deleted=True)
