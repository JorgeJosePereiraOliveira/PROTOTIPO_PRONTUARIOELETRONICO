from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.audit.audit_event_repository_interface import AuditEventRepositoryInterface


@dataclass
class FindAuditEventInputDTO:
    id: str


@dataclass
class FindAuditEventOutputDTO:
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


class FindAuditEventUseCase(UseCase[FindAuditEventInputDTO, FindAuditEventOutputDTO | None]):
    def __init__(self, repository: AuditEventRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: FindAuditEventInputDTO) -> FindAuditEventOutputDTO | None:
        entity = self._repository.find_by_id(input_dto.id)
        if entity is None:
            return None

        return FindAuditEventOutputDTO(
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
