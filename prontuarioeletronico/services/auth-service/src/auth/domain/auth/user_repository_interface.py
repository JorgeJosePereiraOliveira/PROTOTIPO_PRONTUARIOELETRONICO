from typing import Optional

from ..__seedwork.repository_interface import RepositoryInterface
from .user_entity import User


class UserRepositoryInterface(RepositoryInterface[User]):
    def find_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError
