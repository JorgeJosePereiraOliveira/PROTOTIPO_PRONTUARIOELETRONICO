
from abc import ABC, abstractmethod
from .appointment_entity import Appointment

class AppointmentRepositoryInterface(ABC):
	@abstractmethod
	def save(self, appointment: Appointment):
		pass

	@abstractmethod
	def update(self, appointment: Appointment):
		pass

	@abstractmethod
	def find_by_id(self, appointment_id: str) -> Appointment:
		pass

	@abstractmethod
	def delete(self, appointment_id: str):
		pass
