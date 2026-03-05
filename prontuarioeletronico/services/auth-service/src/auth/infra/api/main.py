import os
from datetime import datetime, timezone

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from ...application.auth.authenticate_user_usecase import (
    AuthenticateUserInputDTO,
    AuthenticateUserUseCase,
)
from ...application.auth.logout_usecase import LogoutInputDTO, LogoutUseCase
from ...application.auth.refresh_access_token_usecase import (
    RefreshAccessTokenInputDTO,
    RefreshAccessTokenUseCase,
)
from ...application.auth.authorize_role_usecase import (
    AuthorizeRoleInputDTO,
    AuthorizeRoleUseCase,
)
from ..auth.bcrypt_password_hasher import BcryptPasswordHasher
from ..auth.database import SessionLocal, init_database
from ..auth.jwt_token_service import JwtTokenService
from ..auth.sqlalchemy_access_token_blacklist_repository import (
    SqlAlchemyAccessTokenBlacklistRepository,
)
from ..auth.sqlalchemy_refresh_token_repository import SqlAlchemyRefreshTokenRepository
from ..auth.sqlalchemy_user_repository import SqlAlchemyUserRepository


app = FastAPI(
    title="Auth Service",
    version="1.0.0",
    description="Serviço de autenticação (JWT + RBAC) em Clean Architecture",
)


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


JWT_SECRET = os.getenv("AUTH_JWT_SECRET")
APP_ENV = os.getenv("APP_ENV", "development")

if not JWT_SECRET:
    raise RuntimeError(
        f"AUTH_JWT_SECRET is required for environment '{APP_ENV}'"
    )

init_database()
_db_session = SessionLocal()
_user_repository = SqlAlchemyUserRepository(_db_session)
_refresh_token_repository = SqlAlchemyRefreshTokenRepository(_db_session)
_access_token_blacklist_repository = SqlAlchemyAccessTokenBlacklistRepository(_db_session)
_password_hasher = BcryptPasswordHasher()
_token_service = JwtTokenService(secret_key=JWT_SECRET)
_authenticate_user_usecase = AuthenticateUserUseCase(
    user_repository=_user_repository,
    password_hasher=_password_hasher,
    token_service=_token_service,
    refresh_token_repository=_refresh_token_repository,
)
_authorize_role_usecase = AuthorizeRoleUseCase(token_service=_token_service)
_refresh_access_token_usecase = RefreshAccessTokenUseCase(
    token_service=_token_service,
    refresh_token_repository=_refresh_token_repository,
)
_logout_usecase = LogoutUseCase(
    token_service=_token_service,
    refresh_token_repository=_refresh_token_repository,
    access_blacklist_repository=_access_token_blacklist_repository,
)


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="missing authorization header")

    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise HTTPException(status_code=401, detail="invalid authorization scheme")

    token = authorization[len(prefix):].strip()
    if not token:
        raise HTTPException(status_code=401, detail="empty bearer token")
    return token


def _validate_active_access_token(token: str) -> dict:
    claims = _token_service.decode_token(token)
    if claims.get("type") != "access":
        raise HTTPException(status_code=401, detail="invalid access token type")

    jti = claims.get("jti")
    if not jti:
        raise HTTPException(status_code=401, detail="invalid access token payload")

    is_blacklisted = _access_token_blacklist_repository.is_blacklisted(
        jti=jti,
        now=datetime.now(timezone.utc),
    )
    if is_blacklisted:
        raise HTTPException(status_code=401, detail="access token revoked")

    return claims


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "auth"}


@app.get("/api/v1/info")
def service_info():
    return {
        "service": "auth",
        "architecture": "clean-architecture",
        "layers": ["domain", "application", "infra"],
        "features": ["jwt", "rbac"],
        "default_users": ["admin", "profissional"],
        "default_roles": ["admin", "profissional"],
    }


@app.post("/api/v1/auth/login")
def login(payload: LoginRequest):
    try:
        output = _authenticate_user_usecase.execute(
            AuthenticateUserInputDTO(
                username=payload.username,
                password=payload.password,
            )
        )
        return {
            "access_token": output.access_token,
            "refresh_token": output.refresh_token,
            "token_type": output.token_type,
            "role": output.role,
        }
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error


@app.get("/api/v1/auth/verify")
def verify_token(authorization: str | None = Header(default=None)):
    token = _extract_bearer_token(authorization)
    try:
        claims = _validate_active_access_token(token)
        return {
            "valid": True,
            "claims": {
                "sub": claims.get("sub"),
                "username": claims.get("username"),
                "role": claims.get("role"),
            },
        }
    except Exception as error:
        raise HTTPException(status_code=401, detail="invalid token") from error


@app.post("/api/v1/auth/refresh")
def refresh_token(payload: RefreshRequest):
    try:
        output = _refresh_access_token_usecase.execute(
            RefreshAccessTokenInputDTO(refresh_token=payload.refresh_token)
        )
        return {
            "access_token": output.access_token,
            "refresh_token": output.refresh_token,
            "token_type": output.token_type,
        }
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error


@app.post("/api/v1/auth/logout")
def logout(payload: LogoutRequest, authorization: str | None = Header(default=None)):
    access_token = None
    if authorization:
        access_token = _extract_bearer_token(authorization)

    try:
        output = _logout_usecase.execute(
            LogoutInputDTO(
                refresh_token=payload.refresh_token,
                access_token=access_token,
            )
        )
        return {"logged_out": output.logged_out}
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error


@app.get("/api/v1/auth/authorize")
def authorize(required_role: str, authorization: str | None = Header(default=None)):
    token = _extract_bearer_token(authorization)
    try:
        _validate_active_access_token(token)
        output = _authorize_role_usecase.execute(
            AuthorizeRoleInputDTO(token=token, required_role=required_role)
        )
        return {
            "authorized": output.authorized,
            "role": output.role,
            "required_role": required_role,
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=401, detail="invalid token") from error
