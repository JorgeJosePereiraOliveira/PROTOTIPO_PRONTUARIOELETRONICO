from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.scheduling.appointment_entity import Appointment
from ...domain.scheduling.appointment_repository_interface import (
    AppointmentRepositoryInterface,
)


@dataclass
class CreateAppointmentInputDTO:
    patient_id: str
    professional_id: str
    scheduled_at: str
    reason: str


@dataclass
class CreateAppointmentOutputDTO:
    id: str
    patient_id: str
    professional_id: str
    scheduled_at: str
    reason: str


class CreateAppointmentUseCase(
    UseCase[CreateAppointmentInputDTO, CreateAppointmentOutputDTO]
):
    def __init__(self, repository: AppointmentRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: CreateAppointmentInputDTO) -> CreateAppointmentOutputDTO:
        patient_id = input_dto.patient_id.strip()
        professional_id = input_dto.professional_id.strip()
        scheduled_at = input_dto.scheduled_at.strip()
        reason = input_dto.reason.strip()

        if not patient_id:
            raise ValueError("patient_id is required")
        if not professional_id:
            raise ValueError("professional_id is required")
        if len(reason) < 3:
            raise ValueError("reason must have at least 3 characters")

        try:
            datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError("scheduled_at must be a valid ISO-8601 datetime") from error

        entity = Appointment(
            id=str(uuid4()),
            patient_id=patient_id,
            professional_id=professional_id,
            scheduled_at=scheduled_at,
            reason=reason,
        )
        self._repository.add(entity)

        return CreateAppointmentOutputDTO(
            id=entity.id,
            patient_id=entity.patient_id,
            professional_id=entity.professional_id,
            scheduled_at=entity.scheduled_at,
            reason=entity.reason,
        )
