from dataclasses import dataclass
from datetime import datetime, timezone

from ...domain.__seedwork.use_case_interface import UseCase
from .contracts import RefreshTokenRepository, RefreshTokenState, TokenService


@dataclass
class RefreshAccessTokenInputDTO:
    refresh_token: str


@dataclass
class RefreshAccessTokenOutputDTO:
    access_token: str
    refresh_token: str
    token_type: str


class RefreshAccessTokenUseCase(
    UseCase[RefreshAccessTokenInputDTO, RefreshAccessTokenOutputDTO]
):
    def __init__(
        self,
        token_service: TokenService,
        refresh_token_repository: RefreshTokenRepository,
    ):
        self._token_service = token_service
        self._refresh_token_repository = refresh_token_repository

    def execute(self, input_dto: RefreshAccessTokenInputDTO) -> RefreshAccessTokenOutputDTO:
        if not input_dto.refresh_token:
            raise ValueError("refresh_token is required")

        claims = self._token_service.decode_token(input_dto.refresh_token)
        if claims.get("type") != "refresh":
            raise ValueError("invalid refresh token type")

        jti = claims.get("jti")
        user_id = claims.get("sub")
        username = claims.get("username")
        role = claims.get("role")
        exp_timestamp = claims.get("exp")

        if not all([jti, user_id, username, role, exp_timestamp]):
            raise ValueError("invalid refresh token payload")

        stored_token = self._refresh_token_repository.find_by_jti(jti)
        if stored_token is None:
            raise ValueError("refresh token not found")
        if stored_token.revoked:
            raise ValueError("refresh token revoked")

        expires_at = stored_token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at <= datetime.now(timezone.utc):
            raise ValueError("refresh token expired")

        new_access_token = self._token_service.create_access_token(
            user_id=user_id,
            username=username,
            role=role,
        )
        new_refresh_token = self._token_service.create_refresh_token(
            user_id=user_id,
            username=username,
            role=role,
        )

        new_claims = self._token_service.decode_token(new_refresh_token)
        new_jti = new_claims.get("jti")
        new_exp = new_claims.get("exp")

        if not new_jti or not new_exp:
            raise ValueError("invalid rotated refresh token payload")

        self._refresh_token_repository.revoke(jti, replaced_by_jti=new_jti)
        self._refresh_token_repository.add(
            RefreshTokenState(
                jti=new_jti,
                user_id=user_id,
                username=username,
                role=role,
                expires_at=datetime.fromtimestamp(new_exp, tz=timezone.utc),
                revoked=False,
                replaced_by_jti=None,
            )
        )

        return RefreshAccessTokenOutputDTO(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )
