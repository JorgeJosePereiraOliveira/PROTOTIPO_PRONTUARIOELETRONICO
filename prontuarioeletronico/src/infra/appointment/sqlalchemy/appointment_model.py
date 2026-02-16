"""
SQLAlchemy Model for Appointment
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class AppointmentModel(Base):
    """SQLAlchemy ORM model for Appointment persistence"""
    __tablename__ = "appointments"
    
    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    professional_id = Column(String, ForeignKey("professionals.id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
