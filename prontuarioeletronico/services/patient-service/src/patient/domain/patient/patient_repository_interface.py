from ..__seedwork.repository_interface import RepositoryInterface
from .patient_entity import Patient


class PatientRepositoryInterface(RepositoryInterface[Patient]):
    def find_by_cpf(self, cpf: str) -> Patient | None:
        raise NotImplementedError