from ..__seedwork.entity import Entity


class Appointment(Entity):
    def __init__(
        self,
        id: str,
        patient_id: str,
        professional_id: str,
        scheduled_at: str,
        reason: str,
    ):
        super().__init__(id=id)
        self._patient_id = patient_id
        self._professional_id = professional_id
        self._scheduled_at = scheduled_at
        self._reason = reason

    @property
    def patient_id(self) -> str:
        return self._patient_id

    @property
    def professional_id(self) -> str:
        return self._professional_id

    @property
    def scheduled_at(self) -> str:
        return self._scheduled_at

    @property
    def reason(self) -> str:
        return self._reason
