from datetime import datetime, timedelta, timezone

import jwt

from ...application.auth.contracts import TokenService


class JwtTokenService(TokenService):
    def __init__(self, secret_key: str, algorithm: str = "HS256", expires_minutes: int = 60):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expires_minutes = expires_minutes

    def create_access_token(self, *, user_id: str, username: str, role: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "username": username,
            "role": role,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self._expires_minutes)).timestamp()),
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
