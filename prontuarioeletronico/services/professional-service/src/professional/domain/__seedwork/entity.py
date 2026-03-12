from abc import ABC
from typing import Any


class Entity(ABC):
    def __init__(self, id: Any = None):
        self._id = id

    @property
    def id(self) -> Any:
        return self._id

    @id.setter
    def id(self, value: Any):
        self._id = value

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        if self._id is None or other._id is None:
            return self is other
        return self._id == other._id

    def __hash__(self):
        return hash(self._id) if self._id else hash(id(self))
