from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from ...domain.patient.patient_entity import Patient
from ...domain.patient.patient_repository_interface import PatientRepositoryInterface
from .sqlalchemy_models import PatientModel


class SqlAlchemyPatientRepository(PatientRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: Patient) -> None:
        self._session.add(self._to_model(entity))
        self._session.commit()

    def update(self, entity: Patient) -> None:
        model = self._session.get(PatientModel, entity.id)
        if model is None:
            raise ValueError("patient not found")

        model.name = entity.name
        model.cpf = entity.cpf
        model.date_of_birth = entity.date_of_birth
        model.gender = entity.gender
        self._session.commit()

    def delete(self, id: str) -> None:
        model = self._session.get(PatientModel, id)
        if model is not None:
            self._session.delete(model)
            self._session.commit()

    def find_by_id(self, id: str) -> Optional[Patient]:
        model = self._session.get(PatientModel, id)
        return self._to_entity(model)

    def find_all(self) -> list[Patient]:
        models = self._session.query(PatientModel).all()
        return [self._to_entity(model) for model in models if model is not None]

    def find_by_cpf(self, cpf: str) -> Optional[Patient]:
        model = (
            self._session.query(PatientModel)
            .filter(func.lower(PatientModel.cpf) == cpf.strip().lower())
            .one_or_none()
        )
        return self._to_entity(model)

    def clear(self) -> None:
        self._session.query(PatientModel).delete()
        self._session.commit()

    @staticmethod
    def _to_entity(model: PatientModel | None) -> Optional[Patient]:
        if model is None:
            return None

        return Patient(
            id=model.id,
            name=model.name,
            cpf=model.cpf,
            date_of_birth=model.date_of_birth,
            gender=model.gender,
        )

    @staticmethod
    def _to_model(entity: Patient) -> PatientModel:
        return PatientModel(
            id=entity.id,
            name=entity.name,
            cpf=entity.cpf,
            date_of_birth=entity.date_of_birth,
            gender=entity.gender,
        )