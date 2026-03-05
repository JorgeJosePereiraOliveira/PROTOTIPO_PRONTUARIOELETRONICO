from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
    def create_refresh_token(self, *, user_id: str, username: str, role: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        raise NotImplementedError


@dataclass
class RefreshTokenState:
    jti: str
    user_id: str
    username: str
    role: str
    expires_at: datetime
    revoked: bool
    replaced_by_jti: Optional[str]


class RefreshTokenRepository(ABC):
    @abstractmethod
    def add(self, token_state: RefreshTokenState) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_jti(self, jti: str) -> Optional[RefreshTokenState]:
        raise NotImplementedError

    @abstractmethod
    def revoke(self, jti: str, replaced_by_jti: Optional[str] = None) -> None:
        raise NotImplementedError
