from typing import Optional

from ..__seedwork.repository_interface import RepositoryInterface
from .professional_entity import Professional


class ProfessionalRepositoryInterface(RepositoryInterface[Professional]):
    def find_by_council(
        self,
        council_type: str,
        council_uf: str,
        council_number: str,
    ) -> Optional[Professional]:
        raise NotImplementedError

    def find_all_filtered(
        self,
        council_type: str | None = None,
        council_uf: str | None = None,
        council_number: str | None = None,
        status: str | None = None,
    ) -> list[Professional]:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError
