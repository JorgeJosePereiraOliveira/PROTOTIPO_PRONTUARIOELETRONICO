"""
Use Case: Schedule a new appointment
"""

from datetime import datetime
from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.appointment.appointment_entity import Appointment


class ScheduleAppointmentDTO:
    """Data Transfer Object for scheduling an appointment"""
    
    def __init__(
        self,
        patient_id: str,
        professional_id: str,
        appointment_date: datetime,
        reason: str,
        notes: str = None
    ):
        self.patient_id = patient_id
        self.professional_id = professional_id
        self.appointment_date = appointment_date
        self.reason = reason
        self.notes = notes


class ScheduleAppointmentOutputDTO:
    """Data Transfer Object for appointment scheduling output"""
    
    def __init__(
        self, 
        appointment_id: str, 
        message: str
    ):
        self.appointment_id = appointment_id
        self.message = message


class ScheduleAppointmentUseCase(UseCase[ScheduleAppointmentDTO, ScheduleAppointmentOutputDTO]):
    """
    Use Case for scheduling a new medical appointment.
    """
    
    def __init__(self, appointment_repository):
        self._repository = appointment_repository
    
    def execute(self, input_dto: ScheduleAppointmentDTO) -> ScheduleAppointmentOutputDTO:
        """
        Execute the use case to schedule a new appointment.
        """
        # Validate input
        self._validate_input(input_dto)
        
        # Create appointment entity
        appointment = Appointment(
            id=self._generate_id(),
            patient_id=input_dto.patient_id,
            professional_id=input_dto.professional_id,
            appointment_date=input_dto.appointment_date,
            reason=input_dto.reason,
            notes=input_dto.notes,
            status="scheduled"
        )
        
        # Persist the appointment
        self._repository.add(appointment)
        
        return ScheduleAppointmentOutputDTO(
            appointment_id=appointment.id,
            message=f"Appointment scheduled successfully for {appointment.appointment_date.strftime('%d/%m/%Y %H:%M')}"
        )
    
    def _validate_input(self, input_dto: ScheduleAppointmentDTO):
        """Validate input according to business rules"""
        if not input_dto.patient_id:
            raise ValueError("Patient ID is required")
        if not input_dto.professional_id:
            raise ValueError("Professional ID is required")
        if not input_dto.appointment_date:
            raise ValueError("Appointment date is required")
        if input_dto.appointment_date <= datetime.now():
            raise ValueError("Appointment date must be in the future")
        if not input_dto.reason or len(input_dto.reason) < 3:
            raise ValueError("Appointment reason is required and must be at least 3 characters")
    
    def _generate_id(self) -> str:
        """Generate a unique ID"""
        import uuid
        return str(uuid.uuid4())
