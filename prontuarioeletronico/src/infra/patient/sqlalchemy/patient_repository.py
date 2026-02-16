"""
SQLAlchemy Repository Implementation for Patient
Concrete implementation of the repository interface using SQLAlchemy.
This is part of the Infrastructure layer.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ....domain.patient.patient_entity import Patient
from ....domain.__seedwork.repository_interface import RepositoryInterface
from .patient_model import PatientModel


class PatientRepository(RepositoryInterface[Patient]):
    """
    Concrete repository implementation for Patient using SQLAlchemy.
    
    This repository acts as a bridge between the domain layer (Patient entity)
    and the persistence layer (database). The domain layer doesn't know about
    SQLAlchemy, databases, or any implementation details. This ensures one-way
    dependency: `Patient` depends on `RepositoryInterface`, which is defined in
    the domain layer. The repository implementation depends on both, but the
    domain layer remains clean and testable.
    """
    
    def __init__(self, db: Session):
        self._db = db
    
    def add(self, entity: Patient) -> None:
        """Add a new patient to the database"""
        patient_model = PatientModel(
            id=entity.id,
            name=entity.name,
            date_of_birth=entity.date_of_birth,
            gender=entity.gender,
            cpf=entity.cpf,
            email=entity.email,
            phone=entity.phone,
            address=entity.address,
            city=entity.city,
            state=entity.state,
            insurance=entity.insurance
        )
        self._db.add(patient_model)
        self._db.commit()
        self._db.refresh(patient_model)
    
    def update(self, entity: Patient) -> None:
        """Update an existing patient"""
        patient_model = self._db.query(PatientModel).filter(
            PatientModel.id == entity.id
        ).first()
        if not patient_model:
            raise ValueError(f"Patient with ID {entity.id} not found")
        
        patient_model.name = entity.name
        patient_model.email = entity.email
        patient_model.phone = entity.phone
        patient_model.address = entity.address
        patient_model.city = entity.city
        patient_model.state = entity.state
        patient_model.insurance = entity.insurance
        patient_model.updated_at = datetime.now()
        
        self._db.commit()
        self._db.refresh(patient_model)
    
    def delete(self, id: str) -> None:
        """Delete a patient by ID"""
        patient_model = self._db.query(PatientModel).filter(
            PatientModel.id == id
        ).first()
        if not patient_model:
            raise ValueError(f"Patient with ID {id} not found")
        
        self._db.delete(patient_model)
        self._db.commit()
    
    def find_by_id(self, id: str) -> Optional[Patient]:
        """Find a patient by ID"""
        patient_model = self._db.query(PatientModel).filter(
            PatientModel.id == id
        ).first()
        if not patient_model:
            return None
        return self._to_domain(patient_model)
    
    def find_all(self) -> List[Patient]:
        """Find all patients"""
        patients_models = self._db.query(PatientModel).all()
        return [self._to_domain(p) for p in patients_models]
    
    def find_by_cpf(self, cpf: str) -> Optional[Patient]:
        """Find a patient by CPF"""
        patient_model = self._db.query(PatientModel).filter(
            PatientModel.cpf == cpf
        ).first()
        if not patient_model:
            return None
        return self._to_domain(patient_model)
    
    def _to_domain(self, model: PatientModel) -> Patient:
        """Convert a SQLAlchemy model to a domain entity"""
        return Patient(
            id=model.id,
            name=model.name,
            date_of_birth=model.date_of_birth,
            gender=model.gender,
            cpf=model.cpf,
            email=model.email,
            phone=model.phone,
            address=model.address,
            city=model.city,
            state=model.state,
            insurance=model.insurance,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
