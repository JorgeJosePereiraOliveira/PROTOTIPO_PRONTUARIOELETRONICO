from ..__seedwork.repository_interface import RepositoryInterface
from .consent_entity import Consent


class ConsentRepositoryInterface(RepositoryInterface[Consent]):
    def find_by_patient_id(self, patient_id: str) -> list[Consent]:
        raise NotImplementedError()
