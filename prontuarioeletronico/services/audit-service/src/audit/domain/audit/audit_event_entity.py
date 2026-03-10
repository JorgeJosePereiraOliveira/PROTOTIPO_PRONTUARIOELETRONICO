from ..__seedwork.entity import Entity


class AuditEvent(Entity):
    def __init__(
        self,
        id: str,
        actor_id: str,
        actor_role: str,
        context: str,
        operation: str,
        resource_type: str,
        resource_id: str,
        status: str,
        occurred_at: str,
        metadata: dict | None = None,
    ):
        super().__init__(id=id)
        self._actor_id = actor_id
        self._actor_role = actor_role
        self._context = context
        self._operation = operation
        self._resource_type = resource_type
        self._resource_id = resource_id
        self._status = status
        self._occurred_at = occurred_at
        self._metadata = metadata or {}

    @property
    def actor_id(self) -> str:
        return self._actor_id

    @property
    def actor_role(self) -> str:
        return self._actor_role

    @property
    def context(self) -> str:
        return self._context

    @property
    def operation(self) -> str:
        return self._operation

    @property
    def resource_type(self) -> str:
        return self._resource_type

    @property
    def resource_id(self) -> str:
        return self._resource_id

    @property
    def status(self) -> str:
        return self._status

    @property
    def occurred_at(self) -> str:
        return self._occurred_at

    @property
    def metadata(self) -> dict:
        return self._metadata
