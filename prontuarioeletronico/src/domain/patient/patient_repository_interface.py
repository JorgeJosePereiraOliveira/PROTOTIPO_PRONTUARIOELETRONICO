
from abc import ABC, abstractmethod
from .patient_entity import Patient

class PatientRepositoryInterface(ABC):
	@abstractmethod
	def save(self, patient: Patient):
		pass

	@abstractmethod
	def update(self, patient: Patient):
		pass

	@abstractmethod
	def find_by_id(self, patient_id: str) -> Patient:
		pass

	@abstractmethod
	def delete(self, patient_id: str):
		pass
