
from abc import ABC, abstractmethod
from .professional_entity import Professional

class ProfessionalRepositoryInterface(ABC):
	@abstractmethod
	def save(self, professional: Professional):
		pass

	@abstractmethod
	def update(self, professional: Professional):
		pass

	@abstractmethod
	def find_by_id(self, professional_id: str) -> Professional:
		pass

	@abstractmethod
	def delete(self, professional_id: str):
		pass
