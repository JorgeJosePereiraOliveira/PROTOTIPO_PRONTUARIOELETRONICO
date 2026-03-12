from typing import Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from ...domain.professional.professional_entity import Professional
from ...domain.professional.professional_repository_interface import (
    ProfessionalRepositoryInterface,
)
from .sqlalchemy_models import ProfessionalModel


class SqlAlchemyProfessionalRepository(ProfessionalRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: Professional) -> None:
        self._session.add(self._to_model(entity))
        self._session.commit()

    def update(self, entity: Professional) -> None:
        model = self._session.get(ProfessionalModel, entity.id)
        if model is None:
            raise ValueError("professional not found")

        model.full_name = entity.full_name
        model.document_cpf = entity.document_cpf
        model.council_type = entity.council_type
        model.council_uf = entity.council_uf
        model.council_number = entity.council_number
        model.occupation = entity.occupation
        model.specialty = entity.specialty
        model.auth_user_id = entity.auth_user_id
        model.status = entity.status
        model.updated_at = entity.updated_at
        self._session.commit()

    def delete(self, id: str) -> None:
        model = self._session.get(ProfessionalModel, id)
        if model is not None:
            self._session.delete(model)
            self._session.commit()

    def find_by_id(self, id: str) -> Optional[Professional]:
        model = self._session.get(ProfessionalModel, id)
        return self._to_entity(model)

    def find_all(self) -> list[Professional]:
        models = self._session.query(ProfessionalModel).all()
        return [self._to_entity(model) for model in models if model is not None]

    def find_by_council(
        self,
        council_type: str,
        council_uf: str,
        council_number: str,
    ) -> Optional[Professional]:
        model = (
            self._session.query(ProfessionalModel)
            .filter(
                and_(
                    func.lower(ProfessionalModel.council_type)
                    == council_type.strip().lower(),
                    func.lower(ProfessionalModel.council_uf) == council_uf.strip().lower(),
                    func.lower(ProfessionalModel.council_number)
                    == council_number.strip().lower(),
                )
            )
            .one_or_none()
        )
        return self._to_entity(model)

    def find_all_filtered(
        self,
        council_type: str | None = None,
        council_uf: str | None = None,
        council_number: str | None = None,
        status: str | None = None,
    ) -> list[Professional]:
        query = self._session.query(ProfessionalModel)
        if council_type is not None:
            query = query.filter(
                func.lower(ProfessionalModel.council_type) == council_type.lower()
            )
        if council_uf is not None:
            query = query.filter(func.lower(ProfessionalModel.council_uf) == council_uf.lower())
        if council_number is not None:
            query = query.filter(
                func.lower(ProfessionalModel.council_number) == council_number.lower()
            )
        if status is not None:
            query = query.filter(func.lower(ProfessionalModel.status) == status.lower())

        return [self._to_entity(model) for model in query.all() if model is not None]

    def clear(self) -> None:
        self._session.query(ProfessionalModel).delete()
        self._session.commit()

    @staticmethod
    def _to_entity(model: ProfessionalModel | None) -> Optional[Professional]:
        if model is None:
            return None

        return Professional(
            id=model.id,
            full_name=model.full_name,
            document_cpf=model.document_cpf,
            council_type=model.council_type,
            council_uf=model.council_uf,
            council_number=model.council_number,
            occupation=model.occupation,
            specialty=model.specialty,
            auth_user_id=model.auth_user_id,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(entity: Professional) -> ProfessionalModel:
        return ProfessionalModel(
            id=entity.id,
            full_name=entity.full_name,
            document_cpf=entity.document_cpf,
            council_type=entity.council_type,
            council_uf=entity.council_uf,
            council_number=entity.council_number,
            occupation=entity.occupation,
            specialty=entity.specialty,
            auth_user_id=entity.auth_user_id,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
