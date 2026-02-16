"""
Base Entity class for Clean Architecture.

This module provides a minimal, framework-independent base `Entity` type
that domain objects can inherit from. An entity is an object that has a
stable identity (the `id`) which is used to compare instances and to
implement hashing for use in sets/dicts.

Notes / recommendations:
- Equality (`__eq__`) is based on the `id` value: two entities with the
  same `id` are considered equal.
- Hashing (`__hash__`) uses the `id` when present. If `id` is `None`, the
  instance identity (`id(self)`) is used instead. Mutating the `id` after
  the object has been placed in a hashed collection (set/dict key) may
  break collection invariants. Avoid mutating `id` for objects already
  used as keys or stored in sets.

This file is intentionally small and free of framework concerns so it can
be reused across the domain layer.
"""

from abc import ABC
from typing import Any


class Entity(ABC):
    """Base class for domain entities with an identity.

    Attributes
    - `_id`: the identity of the entity. Can be any hashable type or `None`.

    Behavior summary
    - `id` property: getter/setter for the identity.
    - `__eq__`: two `Entity` instances are equal when they are both
      instances of `Entity` (or subclasses) and their `_id` values are equal.
    - `__hash__`: when `_id` is truthy, `hash(_id)` is used. Otherwise the
      object's memory id is used to provide a stable (per-instance) hash.

    Important: Do not mutate `id` after adding the entity to hashed
    collections. If you need mutable identity semantics, manage hashing and
    equality explicitly in the subclass.
    """

    def __init__(self, id: Any = None):
        """Initialize entity with an optional identity.
        
        Args:
            id: The entity identity. Can be any type. Defaults to None.
        """
        # store identity in a protected attribute to allow subclasses control
        self._id = id

    @property
    def id(self) -> Any:
        """Return the entity identity (may be None)."""
        return self._id

    @id.setter
    def id(self, value: Any):
        """Set or change the entity identity.

        Caution: changing the identity after the instance has been used in
        hashed collections can lead to unexpected behavior.
        
        Args:
            value: The new identity value.
        """
        self._id = value

    def __eq__(self, other):
        """Equality based on entity identity.

        Two entities are equal when both are `Entity` instances and their
        `_id` values compare equal. If `other` is not an Entity, return
        `False`.
        
        Args:
            other: The object to compare with.
            
        Returns:
            bool: True if both are Entity instances with equal id values.
        """
        if not isinstance(other, Entity):
            return False
        return self._id == other._id

    def __hash__(self):
        """Hash based on the identity when available.

        - If `_id` is set (truthy), use `hash(_id)` so equal identities have
          equal hashes.
        - If `_id` is falsy (e.g. `None`), fall back to `hash(id(self))` to
          provide a stable, per-instance hash value.
          
        Returns:
            int: Hash value for the entity.
        """
        return hash(self._id) if self._id else hash(id(self))

    def __repr__(self):
        """Concise representation showing class and identity.
        
        Returns:
            str: String representation like 'Entity(id=123)' or 'Patient(id=None)'.
        """
        return f"{self.__class__.__name__}(id={self._id})"
