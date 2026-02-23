
from abc import ABC, abstractmethod
from .rcop_soap import ClinicalRecord

class ClinicalRecordRepositoryInterface(ABC):
	@abstractmethod
	def save(self, clinical_record: ClinicalRecord):
		pass

	@abstractmethod
	def update(self, clinical_record: ClinicalRecord):
		pass

	@abstractmethod
	def find_by_id(self, clinical_record_id: str) -> ClinicalRecord:
		pass

	@abstractmethod
	def delete(self, clinical_record_id: str):
		pass
