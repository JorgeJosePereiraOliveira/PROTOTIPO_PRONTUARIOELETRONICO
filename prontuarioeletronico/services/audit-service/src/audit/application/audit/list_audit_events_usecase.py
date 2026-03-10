from dataclasses import dataclass
from datetime import datetime

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.audit.audit_event_repository_interface import AuditEventRepositoryInterface


@dataclass
class ListAuditEventsInputDTO:
    actor_id: str | None = None
    operation: str | None = None
    from_datetime: str | None = None
    to_datetime: str | None = None


@dataclass
class AuditEventListItemDTO:
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


@dataclass
class ListAuditEventsOutputDTO:
    events: list[AuditEventListItemDTO]


class ListAuditEventsUseCase(UseCase[ListAuditEventsInputDTO, ListAuditEventsOutputDTO]):
    def __init__(self, repository: AuditEventRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: ListAuditEventsInputDTO) -> ListAuditEventsOutputDTO:
        actor_id = input_dto.actor_id.strip() if input_dto.actor_id else None
        operation = input_dto.operation.strip() if input_dto.operation else None

        from_datetime = None
        if input_dto.from_datetime:
            from_text = input_dto.from_datetime.strip()
            try:
                datetime.fromisoformat(from_text.replace("Z", "+00:00"))
            except ValueError as error:
                raise ValueError("from must be a valid ISO-8601 datetime") from error
            from_datetime = from_text

        to_datetime = None
        if input_dto.to_datetime:
            to_text = input_dto.to_datetime.strip()
            try:
                datetime.fromisoformat(to_text.replace("Z", "+00:00"))
            except ValueError as error:
                raise ValueError("to must be a valid ISO-8601 datetime") from error
            to_datetime = to_text

        entities = self._repository.find_filtered(
            actor_id=actor_id,
            operation=operation,
            from_datetime=from_datetime,
            to_datetime=to_datetime,
        )

        return ListAuditEventsOutputDTO(
            events=[
                AuditEventListItemDTO(
                    id=item.id,
                    actor_id=item.actor_id,
                    actor_role=item.actor_role,
                    context=item.context,
                    operation=item.operation,
                    resource_type=item.resource_type,
                    resource_id=item.resource_id,
                    status=item.status,
                    occurred_at=item.occurred_at,
                    metadata=item.metadata,
                )
                for item in entities
            ]
        )
