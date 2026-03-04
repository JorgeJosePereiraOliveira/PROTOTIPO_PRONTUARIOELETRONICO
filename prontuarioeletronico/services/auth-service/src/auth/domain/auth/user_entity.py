from ..__seedwork.entity import Entity
from .role import Role


class User(Entity):
    def __init__(self, id: str, username: str, password_hash: str, role: Role, active: bool = True):
        super().__init__(id=id)
        self._username = username
        self._password_hash = password_hash
        self._role = role
        self._active = active

    @property
    def username(self) -> str:
        return self._username

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def role(self) -> Role:
        return self._role

    @property
    def active(self) -> bool:
        return self._active
