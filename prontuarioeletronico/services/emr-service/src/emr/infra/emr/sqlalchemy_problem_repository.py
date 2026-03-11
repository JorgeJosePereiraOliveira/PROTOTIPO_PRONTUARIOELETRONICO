from typing import Optional

from sqlalchemy.orm import Session

from ...domain.emr.problem_entity import Problem
from ...domain.emr.problem_repository_interface import ProblemRepositoryInterface
from .sqlalchemy_models import ProblemModel


class SqlAlchemyProblemRepository(ProblemRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: Problem) -> None:
        self._session.add(self._to_model(entity))
        self._session.commit()

    def update(self, entity: Problem) -> None:
        model = self._session.get(ProblemModel, entity.id)
        if model is None:
            raise ValueError("problem not found")

        model.patient_id = entity.patient_id
        model.description = entity.description
        model.terminology_system = entity.terminology_system
        model.terminology_code = entity.terminology_code
        model.status = entity.status
        model.created_at = entity.created_at
        self._session.commit()

    def delete(self, id: str) -> None:
        model = self._session.get(ProblemModel, id)
        if model is not None:
            self._session.delete(model)
            self._session.commit()

    def find_by_id(self, id: str) -> Optional[Problem]:
        model = self._session.get(ProblemModel, id)
        return self._to_entity(model)

    def find_all(self) -> list[Problem]:
        models = self._session.query(ProblemModel).all()
        return [self._to_entity(model) for model in models if model is not None]

    def clear(self) -> None:
        self._session.query(ProblemModel).delete()
        self._session.commit()

    @staticmethod
    def _to_entity(model: ProblemModel | None) -> Optional[Problem]:
        if model is None:
            return None

        return Problem(
            id=model.id,
            patient_id=model.patient_id,
            description=model.description,
            terminology_system=model.terminology_system,
            terminology_code=model.terminology_code,
            status=model.status,
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(entity: Problem) -> ProblemModel:
        return ProblemModel(
            id=entity.id,
            patient_id=entity.patient_id,
            description=entity.description,
            terminology_system=entity.terminology_system,
            terminology_code=entity.terminology_code,
            status=entity.status,
            created_at=entity.created_at,
        )
