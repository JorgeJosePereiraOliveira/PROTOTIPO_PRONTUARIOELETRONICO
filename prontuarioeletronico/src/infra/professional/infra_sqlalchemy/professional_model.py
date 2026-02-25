"""
SQLAlchemy Model for Professional
This is the persistence detail, not part of the domain layer.
It adapts the domain entity to the database schema.
"""

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from prontuarioeletronico.src.infra.infra_sqlalchemy.base import Base


class ProfessionalModel(Base):
    """
    SQLAlchemy ORM model for Professional persistence.
    """
    __tablename__ = "professionals"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    specialties = Column(Text, nullable=True)  # Store as comma-separated string
    crm = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    institution = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def get_specialties_list(self):
        if self.specialties:
            return self.specialties.split(',')
        return []

    def set_specialties_list(self, specialties_list):
        self.specialties = ','.join(specialties_list)
