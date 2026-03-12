from datetime import datetime, timezone

from ..__seedwork.entity import Entity


class Professional(Entity):
    def __init__(
        self,
        id: str,
        full_name: str,
        document_cpf: str,
        council_type: str,
        council_uf: str,
        council_number: str,
        occupation: str,
        specialty: str | None,
        auth_user_id: str | None,
        status: str,
        created_at: str,
        updated_at: str,
    ):
        super().__init__(id=id)
        self._full_name = full_name
        self._document_cpf = document_cpf
        self._council_type = council_type
        self._council_uf = council_uf
        self._council_number = council_number
        self._occupation = occupation
        self._specialty = specialty
        self._auth_user_id = auth_user_id
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def document_cpf(self) -> str:
        return self._document_cpf

    @property
    def council_type(self) -> str:
        return self._council_type

    @property
    def council_uf(self) -> str:
        return self._council_uf

    @property
    def council_number(self) -> str:
        return self._council_number

    @property
    def occupation(self) -> str:
        return self._occupation

    @property
    def specialty(self) -> str | None:
        return self._specialty

    @property
    def auth_user_id(self) -> str | None:
        return self._auth_user_id

    @property
    def status(self) -> str:
        return self._status

    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def updated_at(self) -> str:
        return self._updated_at

    def activate(self) -> None:
        self._status = "active"
        self._updated_at = _iso_utc_now()

    def deactivate(self) -> None:
        self._status = "inactive"
        self._updated_at = _iso_utc_now()


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
