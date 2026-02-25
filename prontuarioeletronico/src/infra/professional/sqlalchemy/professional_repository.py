"""
SQLAlchemy Repository Implementation for Professional
Concrete implementation of the repository interface using SQLAlchemy.
This is part of the Infrastructure layer.
"""

from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from ....domain.professional.professional_entity import Professional
from ....domain.professional.professional_repository_interface import ProfessionalRepositoryInterface
from .professional_model import ProfessionalModel

class ProfessionalRepository(ProfessionalRepositoryInterface):
    """
    Concrete repository implementation for Professional using SQLAlchemy.
    """
    def __init__(self, db: Session):
        self._db = db

    def save(self, professional: Professional):
        model = ProfessionalModel(
            id=professional.id,
            name=professional.name,
            license_number=professional.license_number,
            specialties=','.join(professional.specialties),
            crm=professional.crm,
            email=professional.email,
            phone=professional.phone,
            institution=professional.institution,
            created_at=professional.created_at,
            updated_at=professional.updated_at
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)

    def update(self, professional: Professional):
        model = self._db.query(ProfessionalModel).filter(ProfessionalModel.id == professional.id).first()
        if not model:
            raise ValueError(f"Professional with ID {professional.id} not found")
        model.name = professional.name
        model.license_number = professional.license_number
        model.specialties = ','.join(professional.specialties)
        model.crm = professional.crm
        model.email = professional.email
        model.phone = professional.phone
        model.institution = professional.institution
        model.updated_at = datetime.now()
        self._db.commit()
        self._db.refresh(model)

    def find_by_id(self, professional_id: str) -> Optional[Professional]:
        model = self._db.query(ProfessionalModel).filter(ProfessionalModel.id == professional_id).first()
        if not model:
            return None
        return self._to_domain(model)

    def delete(self, professional_id: str):
        model = self._db.query(ProfessionalModel).filter(ProfessionalModel.id == professional_id).first()
        if not model:
            raise ValueError(f"Professional with ID {professional_id} not found")
        self._db.delete(model)
        self._db.commit()

    def _to_domain(self, model: ProfessionalModel) -> Professional:
        return Professional(
            id=model.id,
            name=model.name,
            license_number=model.license_number,
            specialties=model.get_specialties_list(),
            crm=model.crm,
            email=model.email,
            phone=model.phone,
            institution=model.institution,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
