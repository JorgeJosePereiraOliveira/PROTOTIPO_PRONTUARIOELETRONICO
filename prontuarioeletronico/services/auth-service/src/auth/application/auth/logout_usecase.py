from dataclasses import dataclass
from datetime import datetime, timezone

from ...domain.__seedwork.use_case_interface import UseCase
from .contracts import (
    AccessTokenBlacklistRepository,
    AccessTokenBlacklistState,
    RefreshTokenRepository,
    TokenService,
)


@dataclass
class LogoutInputDTO:
    refresh_token: str
    access_token: str | None = None


@dataclass
class LogoutOutputDTO:
    logged_out: bool


class LogoutUseCase(UseCase[LogoutInputDTO, LogoutOutputDTO]):
    def __init__(
        self,
        token_service: TokenService,
        refresh_token_repository: RefreshTokenRepository,
        access_blacklist_repository: AccessTokenBlacklistRepository,
    ):
        self._token_service = token_service
        self._refresh_token_repository = refresh_token_repository
        self._access_blacklist_repository = access_blacklist_repository

    def execute(self, input_dto: LogoutInputDTO) -> LogoutOutputDTO:
        if not input_dto.refresh_token:
            raise ValueError("refresh_token is required")

        refresh_claims = self._token_service.decode_token(input_dto.refresh_token)
        if refresh_claims.get("type") != "refresh":
            raise ValueError("invalid refresh token type")

        refresh_jti = refresh_claims.get("jti")
        if not refresh_jti:
            raise ValueError("invalid refresh token payload")

        refresh_state = self._refresh_token_repository.find_by_jti(refresh_jti)
        if refresh_state is None:
            raise ValueError("refresh token not found")

        if not refresh_state.revoked:
            self._refresh_token_repository.revoke(refresh_jti)

        if input_dto.access_token:
            access_claims = self._token_service.decode_token(input_dto.access_token)
            if access_claims.get("type") != "access":
                raise ValueError("invalid access token type")

            access_jti = access_claims.get("jti")
            access_exp = access_claims.get("exp")
            if not access_jti or not access_exp:
                raise ValueError("invalid access token payload")

            expires_at = datetime.fromtimestamp(access_exp, tz=timezone.utc)
            if expires_at > datetime.now(timezone.utc):
                self._access_blacklist_repository.add(
                    AccessTokenBlacklistState(
                        jti=access_jti,
                        expires_at=expires_at,
                    )
                )

        return LogoutOutputDTO(logged_out=True)
