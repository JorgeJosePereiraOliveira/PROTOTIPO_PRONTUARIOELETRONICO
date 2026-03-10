from typing import Optional

from sqlalchemy.orm import Session

from ...domain.scheduling.appointment_entity import Appointment
from ...domain.scheduling.appointment_repository_interface import (
    AppointmentRepositoryInterface,
)
from .sqlalchemy_models import AppointmentModel


class SqlAlchemyAppointmentRepository(AppointmentRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: Appointment) -> None:
        self._session.add(self._to_model(entity))
        self._session.commit()

    def update(self, entity: Appointment) -> None:
        model = self._session.get(AppointmentModel, entity.id)
        if model is None:
            raise ValueError("appointment not found")

        model.patient_id = entity.patient_id
        model.professional_id = entity.professional_id
        model.scheduled_at = entity.scheduled_at
        model.reason = entity.reason
        self._session.commit()

    def delete(self, id: str) -> None:
        model = self._session.get(AppointmentModel, id)
        if model is not None:
            self._session.delete(model)
            self._session.commit()

    def find_by_id(self, id: str) -> Optional[Appointment]:
        model = self._session.get(AppointmentModel, id)
        return self._to_entity(model)

    def find_all(self) -> list[Appointment]:
        models = self._session.query(AppointmentModel).all()
        return [self._to_entity(model) for model in models if model is not None]

    def clear(self) -> None:
        self._session.query(AppointmentModel).delete()
        self._session.commit()

    @staticmethod
    def _to_entity(model: AppointmentModel | None) -> Optional[Appointment]:
        if model is None:
            return None

        return Appointment(
            id=model.id,
            patient_id=model.patient_id,
            professional_id=model.professional_id,
            scheduled_at=model.scheduled_at,
            reason=model.reason,
        )

    @staticmethod
    def _to_model(entity: Appointment) -> AppointmentModel:
        return AppointmentModel(
            id=entity.id,
            patient_id=entity.patient_id,
            professional_id=entity.professional_id,
            scheduled_at=entity.scheduled_at,
            reason=entity.reason,
        )
