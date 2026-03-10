from ..__seedwork.repository_interface import RepositoryInterface
from .audit_event_entity import AuditEvent


class AuditEventRepositoryInterface(RepositoryInterface[AuditEvent]):
    pass
