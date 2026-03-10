from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.scheduling.appointment_repository_interface import (
    AppointmentRepositoryInterface,
)


@dataclass
class AppointmentListItemDTO:
    id: str
    patient_id: str
    professional_id: str
    scheduled_at: str
    reason: str


@dataclass
class ListAppointmentsOutputDTO:
    appointments: list[AppointmentListItemDTO]


class ListAppointmentsUseCase(UseCase[None, ListAppointmentsOutputDTO]):
    def __init__(self, repository: AppointmentRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: None) -> ListAppointmentsOutputDTO:
        entities = self._repository.find_all()
        return ListAppointmentsOutputDTO(
            appointments=[
                AppointmentListItemDTO(
                    id=item.id,
                    patient_id=item.patient_id,
                    professional_id=item.professional_id,
                    scheduled_at=item.scheduled_at,
                    reason=item.reason,
                )
                for item in entities
            ]
        )
