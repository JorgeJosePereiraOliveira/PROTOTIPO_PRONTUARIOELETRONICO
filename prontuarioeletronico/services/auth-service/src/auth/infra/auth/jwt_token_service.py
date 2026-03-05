from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt

from ...application.auth.contracts import TokenService


class JwtTokenService(TokenService):
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_expires_minutes: int = 15,
        refresh_expires_minutes: int = 60 * 24 * 7,
    ):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._access_expires_minutes = access_expires_minutes
        self._refresh_expires_minutes = refresh_expires_minutes

    def create_access_token(self, *, user_id: str, username: str, role: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "username": username,
            "role": role,
            "type": "access",
            "jti": str(uuid4()),
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self._access_expires_minutes)).timestamp()),
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def create_refresh_token(self, *, user_id: str, username: str, role: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "username": username,
            "role": role,
            "type": "refresh",
            "jti": str(uuid4()),
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self._refresh_expires_minutes)).timestamp()),
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
