"""
SQLAlchemy Model for Patient
This is the persistence detail, not part of the domain layer.
It adapts the domain entity to the database schema.
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class PatientModel(Base):
    """
    SQLAlchemy ORM model for Patient persistence.
    
    This model is part of the Infrastructure layer and should NOT be
    used directly in the domain or application layers. It's an adapter
    that converts between the database schema and domain entities.
    """
    __tablename__ = "patients"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    insurance = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
