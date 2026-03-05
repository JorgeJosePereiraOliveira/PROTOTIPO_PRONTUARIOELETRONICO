from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ...application.auth.contracts import (
    AccessTokenBlacklistRepository,
    AccessTokenBlacklistState,
)
from .sqlalchemy_models import AccessTokenBlacklistModel


class SqlAlchemyAccessTokenBlacklistRepository(AccessTokenBlacklistRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, token_state: AccessTokenBlacklistState) -> None:
        existing = self._session.get(AccessTokenBlacklistModel, token_state.jti)
        if existing is None:
            self._session.add(
                AccessTokenBlacklistModel(
                    jti=token_state.jti,
                    expires_at=token_state.expires_at,
                )
            )
            self._session.commit()

    def is_blacklisted(self, jti: str, now: datetime) -> bool:
        model = self._session.get(AccessTokenBlacklistModel, jti)
        if model is None:
            return False

        expires_at = model.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at <= now:
            self._session.delete(model)
            self._session.commit()
            return False

        return True
