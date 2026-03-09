from ..__seedwork.entity import Entity


class Problem(Entity):
    def __init__(self, id: str, patient_id: str, description: str, status: str = "active"):
        super().__init__(id=id)
        self._patient_id = patient_id
        self._description = description
        self._status = status

    @property
    def patient_id(self) -> str:
        return self._patient_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def status(self) -> str:
        return self._status
