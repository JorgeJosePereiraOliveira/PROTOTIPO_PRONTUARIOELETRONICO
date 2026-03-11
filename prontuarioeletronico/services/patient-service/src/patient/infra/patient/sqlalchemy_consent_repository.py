from typing import Optional

from sqlalchemy.orm import Session

from ...domain.consent.consent_entity import Consent
from ...domain.consent.consent_repository_interface import ConsentRepositoryInterface
from .sqlalchemy_models import ConsentModel


class SqlAlchemyConsentRepository(ConsentRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: Consent) -> None:
        self._session.add(self._to_model(entity))
        self._session.commit()

    def update(self, entity: Consent) -> None:
        model = self._session.get(ConsentModel, entity.id)
        if model is None:
            raise ValueError("consent not found")

        model.patient_id = entity.patient_id
        model.legal_basis = entity.legal_basis
        model.purpose = entity.purpose
        model.status = entity.status
        model.granted_at = entity.granted_at
        model.revoked_at = entity.revoked_at
        self._session.commit()

    def delete(self, id: str) -> None:
        model = self._session.get(ConsentModel, id)
        if model is not None:
            self._session.delete(model)
            self._session.commit()

    def find_by_id(self, id: str) -> Optional[Consent]:
        model = self._session.get(ConsentModel, id)
        return self._to_entity(model)

    def find_all(self) -> list[Consent]:
        models = self._session.query(ConsentModel).all()
        return [self._to_entity(model) for model in models if model is not None]

    def find_by_patient_id(self, patient_id: str) -> list[Consent]:
        models = (
            self._session.query(ConsentModel)
            .filter(ConsentModel.patient_id == patient_id)
            .all()
        )
        return [self._to_entity(model) for model in models if model is not None]

    def clear(self) -> None:
        self._session.query(ConsentModel).delete()
        self._session.commit()

    @staticmethod
    def _to_entity(model: ConsentModel | None) -> Optional[Consent]:
        if model is None:
            return None

        return Consent(
            id=model.id,
            patient_id=model.patient_id,
            legal_basis=model.legal_basis,
            purpose=model.purpose,
            status=model.status,
            granted_at=model.granted_at,
            revoked_at=model.revoked_at,
        )

    @staticmethod
    def _to_model(entity: Consent) -> ConsentModel:
        return ConsentModel(
            id=entity.id,
            patient_id=entity.patient_id,
            legal_basis=entity.legal_basis,
            purpose=entity.purpose,
            status=entity.status,
            granted_at=entity.granted_at,
            revoked_at=entity.revoked_at,
        )
