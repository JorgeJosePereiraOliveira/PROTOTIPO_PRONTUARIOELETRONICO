from typing import Optional

from sqlalchemy.orm import Session

from ...application.auth.contracts import RefreshTokenRepository, RefreshTokenState
from .sqlalchemy_models import RefreshTokenModel


class SqlAlchemyRefreshTokenRepository(RefreshTokenRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, token_state: RefreshTokenState) -> None:
        model = RefreshTokenModel(
            jti=token_state.jti,
            user_id=token_state.user_id,
            username=token_state.username,
            role=token_state.role,
            expires_at=token_state.expires_at,
            revoked=token_state.revoked,
            replaced_by_jti=token_state.replaced_by_jti,
        )
        self._session.add(model)
        self._session.commit()

    def find_by_jti(self, jti: str) -> Optional[RefreshTokenState]:
        model = self._session.get(RefreshTokenModel, jti)
        if model is None:
            return None

        return RefreshTokenState(
            jti=model.jti,
            user_id=model.user_id,
            username=model.username,
            role=model.role,
            expires_at=model.expires_at,
            revoked=model.revoked,
            replaced_by_jti=model.replaced_by_jti,
        )

    def revoke(self, jti: str, replaced_by_jti: str | None = None) -> None:
        model = self._session.get(RefreshTokenModel, jti)
        if model is None:
            raise ValueError("refresh token not found")

        model.revoked = True
        model.replaced_by_jti = replaced_by_jti
        self._session.commit()
