from datetime import datetime, timezone

from ..__seedwork.entity import Entity


class Consent(Entity):
    def __init__(
        self,
        id: str,
        patient_id: str,
        legal_basis: str,
        purpose: str,
        status: str,
        granted_at: str,
        revoked_at: str | None = None,
    ):
        super().__init__(id=id)
        self._patient_id = patient_id
        self._legal_basis = legal_basis
        self._purpose = purpose
        self._status = status
        self._granted_at = granted_at
        self._revoked_at = revoked_at

    @property
    def patient_id(self) -> str:
        return self._patient_id

    @property
    def legal_basis(self) -> str:
        return self._legal_basis

    @property
    def purpose(self) -> str:
        return self._purpose

    @property
    def status(self) -> str:
        return self._status

    @property
    def granted_at(self) -> str:
        return self._granted_at

    @property
    def revoked_at(self) -> str | None:
        return self._revoked_at

    @staticmethod
    def utc_now_iso() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
