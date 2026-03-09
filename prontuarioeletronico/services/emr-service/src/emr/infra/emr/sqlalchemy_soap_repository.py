from typing import Optional

from sqlalchemy.orm import Session

from ...domain.emr.soap_record_entity import SOAPRecord
from ...domain.emr.soap_repository_interface import SOAPRepositoryInterface
from .sqlalchemy_models import SOAPRecordModel


class SqlAlchemySOAPRepository(SOAPRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: SOAPRecord) -> None:
        self._session.add(self._to_model(entity))
        self._session.commit()

    def update(self, entity: SOAPRecord) -> None:
        model = self._session.get(SOAPRecordModel, entity.id)
        if model is None:
            raise ValueError("soap record not found")

        model.problem_id = entity.problem_id
        model.patient_id = entity.patient_id
        model.professional_id = entity.professional_id
        model.subjective = entity.subjective
        model.objective = entity.objective
        model.assessment = entity.assessment
        model.plan = entity.plan
        self._session.commit()

    def delete(self, id: str) -> None:
        model = self._session.get(SOAPRecordModel, id)
        if model is not None:
            self._session.delete(model)
            self._session.commit()

    def find_by_id(self, id: str) -> Optional[SOAPRecord]:
        model = self._session.get(SOAPRecordModel, id)
        return self._to_entity(model)

    def find_all(self) -> list[SOAPRecord]:
        models = self._session.query(SOAPRecordModel).all()
        return [self._to_entity(model) for model in models if model is not None]

    def clear(self) -> None:
        self._session.query(SOAPRecordModel).delete()
        self._session.commit()

    @staticmethod
    def _to_entity(model: SOAPRecordModel | None) -> Optional[SOAPRecord]:
        if model is None:
            return None

        return SOAPRecord(
            id=model.id,
            problem_id=model.problem_id,
            patient_id=model.patient_id,
            professional_id=model.professional_id,
            subjective=model.subjective,
            objective=model.objective,
            assessment=model.assessment,
            plan=model.plan,
        )

    @staticmethod
    def _to_model(entity: SOAPRecord) -> SOAPRecordModel:
        return SOAPRecordModel(
            id=entity.id,
            problem_id=entity.problem_id,
            patient_id=entity.patient_id,
            professional_id=entity.professional_id,
            subjective=entity.subjective,
            objective=entity.objective,
            assessment=entity.assessment,
            plan=entity.plan,
        )
