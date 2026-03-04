from typing import Optional

from ...domain.auth.role import Role
from ...domain.auth.user_entity import User
from ...domain.auth.user_repository_interface import UserRepositoryInterface
from .bcrypt_password_hasher import BcryptPasswordHasher


class InMemoryUserRepository(UserRepositoryInterface):
    def __init__(self):
        hasher = BcryptPasswordHasher()
        self._data: dict[str, User] = {
            "u-admin": User(
                id="u-admin",
                username="admin",
                password_hash=hasher.hash("admin123"),
                role=Role.ADMIN,
                active=True,
            ),
            "u-prof": User(
                id="u-prof",
                username="profissional",
                password_hash=hasher.hash("prof123"),
                role=Role.PROFESSIONAL,
                active=True,
            ),
        }

    def add(self, entity: User) -> None:
        self._data[entity.id] = entity

    def update(self, entity: User) -> None:
        self._data[entity.id] = entity

    def delete(self, id: str) -> None:
        self._data.pop(id, None)

    def find_by_id(self, id: str) -> Optional[User]:
        return self._data.get(id)

    def find_all(self) -> list[User]:
        return list(self._data.values())

    def find_by_username(self, username: str) -> Optional[User]:
        username_normalized = username.strip().lower()
        for user in self._data.values():
            if user.username.lower() == username_normalized:
                return user
        return None
