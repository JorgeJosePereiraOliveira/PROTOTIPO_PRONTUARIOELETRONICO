from typing import Optional

from sqlalchemy.orm import Session

from ...domain.audit.audit_event_entity import AuditEvent
from ...domain.audit.audit_event_repository_interface import AuditEventRepositoryInterface
from .sqlalchemy_models import AuditEventModel


class SqlAlchemyAuditEventRepository(AuditEventRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: AuditEvent) -> None:
        self._session.add(self._to_model(entity))
        self._session.commit()

    def update(self, entity: AuditEvent) -> None:
        model = self._session.get(AuditEventModel, entity.id)
        if model is None:
            raise ValueError("audit event not found")

        model.actor_id = entity.actor_id
        model.actor_role = entity.actor_role
        model.context = entity.context
        model.operation = entity.operation
        model.resource_type = entity.resource_type
        model.resource_id = entity.resource_id
        model.status = entity.status
        model.occurred_at = entity.occurred_at
        model.metadata_json = entity.metadata
        self._session.commit()

    def delete(self, id: str) -> None:
        model = self._session.get(AuditEventModel, id)
        if model is not None:
            self._session.delete(model)
            self._session.commit()

    def find_by_id(self, id: str) -> Optional[AuditEvent]:
        model = self._session.get(AuditEventModel, id)
        return self._to_entity(model)

    def find_all(self) -> list[AuditEvent]:
        models = self._session.query(AuditEventModel).all()
        return [self._to_entity(model) for model in models if model is not None]

    def find_filtered(
        self,
        actor_id: str | None = None,
        operation: str | None = None,
        from_datetime: str | None = None,
        to_datetime: str | None = None,
    ) -> list[AuditEvent]:
        query = self._session.query(AuditEventModel)

        if actor_id:
            query = query.filter(AuditEventModel.actor_id == actor_id)
        if operation:
            query = query.filter(AuditEventModel.operation == operation)
        if from_datetime:
            query = query.filter(AuditEventModel.occurred_at >= from_datetime)
        if to_datetime:
            query = query.filter(AuditEventModel.occurred_at <= to_datetime)

        models = query.order_by(AuditEventModel.occurred_at.desc()).all()
        return [self._to_entity(model) for model in models if model is not None]

    def clear(self) -> None:
        self._session.query(AuditEventModel).delete()
        self._session.commit()

    @staticmethod
    def _to_entity(model: AuditEventModel | None) -> Optional[AuditEvent]:
        if model is None:
            return None

        return AuditEvent(
            id=model.id,
            actor_id=model.actor_id,
            actor_role=model.actor_role,
            context=model.context,
            operation=model.operation,
            resource_type=model.resource_type,
            resource_id=model.resource_id,
            status=model.status,
            occurred_at=model.occurred_at,
            metadata=model.metadata_json or {},
        )

    @staticmethod
    def _to_model(entity: AuditEvent) -> AuditEventModel:
        return AuditEventModel(
            id=entity.id,
            actor_id=entity.actor_id,
            actor_role=entity.actor_role,
            context=entity.context,
            operation=entity.operation,
            resource_type=entity.resource_type,
            resource_id=entity.resource_id,
            status=entity.status,
            occurred_at=entity.occurred_at,
            metadata_json=entity.metadata,
        )
