from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from .entity import Entity


Entity_T = TypeVar("Entity_T", bound=Entity)


class RepositoryInterface(ABC, Generic[Entity_T]):
    @abstractmethod
    def add(self, entity: Entity_T) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: Entity_T) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Entity_T]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Entity_T]:
        raise NotImplementedError
