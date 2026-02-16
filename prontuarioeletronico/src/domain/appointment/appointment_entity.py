"""
Appointment Domain Entity - Represents a medical appointment
"""

from typing import Optional
from datetime import datetime
from ...__seedwork.entity import Entity


class Appointment(Entity):
    """
    Represents a medical appointment in the electronic patient record system.
    
    This entity encapsulates the core attributes and business rules
    related to clinical appointments/consultations.
    
    Attributes:
        id: Unique identifier
        patient_id: Reference to the patient
        professional_id: Reference to the healthcare professional
        appointment_date: Date and time of the appointment
        reason: Reason for the appointment
        status: Appointment status (scheduled, completed, cancelled)
        notes: Additional notes about the appointment
        created_at: Record creation timestamp
        updated_at: Record update timestamp
    """
    
    def __init__(
        self,
        id: str,
        patient_id: str,
        professional_id: str,
        appointment_date: datetime,
        reason: str,
        status: str = "scheduled",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        super().__init__(id)
        self._patient_id = patient_id
        self._professional_id = professional_id
        self._appointment_date = appointment_date
        self._reason = reason
        self._status = status  # scheduled, completed, cancelled
        self._notes = notes
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or datetime.now()
    
    @property
    def patient_id(self) -> str:
        return self._patient_id
    
    @property
    def professional_id(self) -> str:
        return self._professional_id
    
    @property
    def appointment_date(self) -> datetime:
        return self._appointment_date
    
    @property
    def reason(self) -> str:
        return self._reason
    
    @property
    def status(self) -> str:
        return self._status
    
    @property
    def notes(self) -> Optional[str]:
        return self._notes
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def mark_completed(self, notes: Optional[str] = None):
        """Mark the appointment as completed."""
        if self._status != "completed":
            self._status = "completed"
            if notes:
                self._notes = notes
            self._updated_at = datetime.now()
    
    def cancel(self, reason: Optional[str] = None):
        """Cancel the appointment."""
        if self._status != "cancelled":
            self._status = "cancelled"
            if reason:
                self._notes = reason
            self._updated_at = datetime.now()
    
    def reschedule(self, new_date: datetime):
        """Reschedule the appointment to a new date."""
        if self._status == "scheduled":
            self._appointment_date = new_date
            self._updated_at = datetime.now()
    
    def is_overdue(self) -> bool:
        """Check if the appointment date has passed."""
        return self._appointment_date < datetime.now() and self._status != "completed"
