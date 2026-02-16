"""
SQLAlchemy Repository Implementation for Appointment
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ....domain.appointment.appointment_entity import Appointment
from ....domain.__seedwork.repository_interface import RepositoryInterface
from .appointment_model import AppointmentModel


class AppointmentRepository(RepositoryInterface[Appointment]):
    """Repository implementation for Appointment persistence"""
    
    def __init__(self, db: Session):
        self._db = db
    
    def add(self, entity: Appointment) -> None:
        """Add a new appointment"""
        model = AppointmentModel(
            id=entity.id,
            patient_id=entity.patient_id,
            professional_id=entity.professional_id,
            appointment_date=entity.appointment_date,
            reason=entity.reason,
            status=entity.status,
            notes=entity.notes
        )
        self._db.add(model)
        self._db.commit()
    
    def update(self, entity: Appointment) -> None:
        """Update an appointment"""
        model = self._db.query(AppointmentModel).filter(
            AppointmentModel.id == entity.id
        ).first()
        if not model:
            raise ValueError(f"Appointment {entity.id} not found")
        
        model.appointment_date = entity.appointment_date
        model.reason = entity.reason
        model.status = entity.status
        model.notes = entity.notes
        model.updated_at = datetime.now()
        
        self._db.commit()
    
    def delete(self, id: str) -> None:
        """Delete an appointment"""
        model = self._db.query(AppointmentModel).filter(
            AppointmentModel.id == id
        ).first()
        if not model:
            raise ValueError(f"Appointment {id} not found")
        
        self._db.delete(model)
        self._db.commit()
    
    def find_by_id(self, id: str) -> Optional[Appointment]:
        """Find an appointment by ID"""
        model = self._db.query(AppointmentModel).filter(
            AppointmentModel.id == id
        ).first()
        if not model:
            return None
        return self._to_domain(model)
    
    def find_all(self) -> List[Appointment]:
        """Find all appointments"""
        models = self._db.query(AppointmentModel).all()
        return [self._to_domain(m) for m in models]
    
    def find_by_patient(self, patient_id: str) -> List[Appointment]:
        """Find appointments for a specific patient"""
        models = self._db.query(AppointmentModel).filter(
            AppointmentModel.patient_id == patient_id
        ).all()
        return [self._to_domain(m) for m in models]
    
    def _to_domain(self, model: AppointmentModel) -> Appointment:
        """Convert SQLAlchemy model to domain entity"""
        return Appointment(
            id=model.id,
            patient_id=model.patient_id,
            professional_id=model.professional_id,
            appointment_date=model.appointment_date,
            reason=model.reason,
            status=model.status,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
