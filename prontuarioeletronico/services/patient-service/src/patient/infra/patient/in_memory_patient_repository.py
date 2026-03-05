from ...domain.patient.patient_entity import Patient
from ...domain.patient.patient_repository_interface import PatientRepositoryInterface


class InMemoryPatientRepository(PatientRepositoryInterface):
    def __init__(self):
        self._data: dict[str, Patient] = {}
        self._cpf_index: dict[str, str] = {}

    def add(self, entity: Patient) -> None:
        self._data[entity.id] = entity
        self._cpf_index[entity.cpf] = entity.id

    def update(self, entity: Patient) -> None:
        current = self._data.get(entity.id)
        if current is not None and current.cpf != entity.cpf:
            self._cpf_index.pop(current.cpf, None)
        self._data[entity.id] = entity
        self._cpf_index[entity.cpf] = entity.id

    def delete(self, id: str) -> None:
        entity = self._data.pop(id, None)
        if entity is not None:
            self._cpf_index.pop(entity.cpf, None)

    def find_by_id(self, id: str) -> Patient | None:
        return self._data.get(id)

    def find_all(self) -> list[Patient]:
        return list(self._data.values())

    def find_by_cpf(self, cpf: str) -> Patient | None:
        patient_id = self._cpf_index.get(cpf)
        if patient_id is None:
            return None
        return self._data.get(patient_id)

    def clear(self) -> None:
        self._data.clear()
        self._cpf_index.clear()