from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.scheduling.appointment_repository_interface import (
    AppointmentRepositoryInterface,
)


@dataclass
class FindAppointmentInputDTO:
    id: str


@dataclass
class FindAppointmentOutputDTO:
    id: str
    patient_id: str
    professional_id: str
    scheduled_at: str
    reason: str


class FindAppointmentUseCase(
    UseCase[FindAppointmentInputDTO, FindAppointmentOutputDTO | None]
):
    def __init__(self, repository: AppointmentRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: FindAppointmentInputDTO) -> FindAppointmentOutputDTO | None:
        entity = self._repository.find_by_id(input_dto.id)
        if entity is None:
            return None

        return FindAppointmentOutputDTO(
            id=entity.id,
            patient_id=entity.patient_id,
            professional_id=entity.professional_id,
            scheduled_at=entity.scheduled_at,
            reason=entity.reason,
        )
