from abc import ABC, abstractmethod
from domain.user.user_entity import User
from typing import List
from uuid import UUID


class UserRepositoryInterface(ABC):

    @abstractmethod
    def add_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_user(self, user_id: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    def update_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_users(self) -> List[User]:
        raise NotImplementedError
