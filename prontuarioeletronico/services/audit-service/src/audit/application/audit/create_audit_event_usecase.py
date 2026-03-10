from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.audit.audit_event_entity import AuditEvent
from ...domain.audit.audit_event_repository_interface import AuditEventRepositoryInterface


@dataclass
class CreateAuditEventInputDTO:
    actor_id: str
    actor_role: str
    context: str
    operation: str
    resource_type: str
    resource_id: str
    status: str
    occurred_at: str
    metadata: dict | None = None


@dataclass
class CreateAuditEventOutputDTO:
    id: str
    actor_id: str
    actor_role: str
    context: str
    operation: str
    resource_type: str
    resource_id: str
    status: str
    occurred_at: str
    metadata: dict


class CreateAuditEventUseCase(UseCase[CreateAuditEventInputDTO, CreateAuditEventOutputDTO]):
    _ALLOWED_STATUS = {"success", "denied", "error"}

    def __init__(self, repository: AuditEventRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: CreateAuditEventInputDTO) -> CreateAuditEventOutputDTO:
        actor_id = input_dto.actor_id.strip()
        actor_role = input_dto.actor_role.strip()
        context = input_dto.context.strip()
        operation = input_dto.operation.strip()
        resource_type = input_dto.resource_type.strip()
        resource_id = input_dto.resource_id.strip()
        status = input_dto.status.strip().lower()
        occurred_at = input_dto.occurred_at.strip()

        for field_name, value in {
            "actor_id": actor_id,
            "actor_role": actor_role,
            "context": context,
            "operation": operation,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "occurred_at": occurred_at,
        }.items():
            if not value:
                raise ValueError(f"{field_name} is required")

        if status not in self._ALLOWED_STATUS:
            raise ValueError("status must be one of: success, denied, error")

        try:
            datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError("occurred_at must be a valid ISO-8601 datetime") from error

        entity = AuditEvent(
            id=str(uuid4()),
            actor_id=actor_id,
            actor_role=actor_role,
            context=context,
            operation=operation,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            occurred_at=occurred_at,
            metadata=input_dto.metadata or {},
        )
        self._repository.add(entity)

        return CreateAuditEventOutputDTO(
            id=entity.id,
            actor_id=entity.actor_id,
            actor_role=entity.actor_role,
            context=entity.context,
            operation=entity.operation,
            resource_type=entity.resource_type,
            resource_id=entity.resource_id,
            status=entity.status,
            occurred_at=entity.occurred_at,
            metadata=entity.metadata,
        )
