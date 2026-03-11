from datetime import datetime, timezone

from ..__seedwork.entity import Entity


class Problem(Entity):
    def __init__(
        self,
        id: str,
        patient_id: str,
        description: str,
        terminology_system: str,
        terminology_code: str,
        status: str = "active",
        created_at: str | None = None,
    ):
        super().__init__(id=id)
        self._patient_id = patient_id
        self._description = description
        self._terminology_system = terminology_system
        self._terminology_code = terminology_code
        self._status = status
        self._created_at = created_at or datetime.now(timezone.utc).isoformat().replace(
            "+00:00", "Z"
        )

    @property
    def patient_id(self) -> str:
        return self._patient_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def terminology_system(self) -> str:
        return self._terminology_system

    @property
    def terminology_code(self) -> str:
        return self._terminology_code

    @property
    def status(self) -> str:
        return self._status

    @property
    def created_at(self) -> str:
        return self._created_at
