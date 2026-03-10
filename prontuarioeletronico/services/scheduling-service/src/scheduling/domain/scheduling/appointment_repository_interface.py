from ..__seedwork.repository_interface import RepositoryInterface
from .appointment_entity import Appointment


class AppointmentRepositoryInterface(RepositoryInterface[Appointment]):
    pass
