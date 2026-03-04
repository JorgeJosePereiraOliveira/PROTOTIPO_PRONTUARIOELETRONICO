from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, plain_password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify(self, plain_password: str, password_hash: str) -> bool:
        raise NotImplementedError


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, *, user_id: str, username: str, role: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        raise NotImplementedError
