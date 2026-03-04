import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from ...application.auth.authenticate_user_usecase import (
    AuthenticateUserInputDTO,
    AuthenticateUserUseCase,
)
from ...application.auth.authorize_role_usecase import (
    AuthorizeRoleInputDTO,
    AuthorizeRoleUseCase,
)
from ..auth.database import SessionLocal, init_database
from ..auth.jwt_token_service import JwtTokenService
from ..auth.sqlalchemy_user_repository import SqlAlchemyUserRepository
from ..auth.sha256_password_hasher import Sha256PasswordHasher


app = FastAPI(
    title="Auth Service",
    version="1.0.0",
    description="Serviço de autenticação (JWT + RBAC) em Clean Architecture",
)


class LoginRequest(BaseModel):
    username: str
    password: str


JWT_SECRET = os.getenv("AUTH_JWT_SECRET", "dev-secret-change-me")

init_database()
_db_session = SessionLocal()
_user_repository = SqlAlchemyUserRepository(_db_session)
_password_hasher = Sha256PasswordHasher()
_token_service = JwtTokenService(secret_key=JWT_SECRET)
_authenticate_user_usecase = AuthenticateUserUseCase(
    user_repository=_user_repository,
    password_hasher=_password_hasher,
    token_service=_token_service,
)
_authorize_role_usecase = AuthorizeRoleUseCase(token_service=_token_service)


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
            "token_type": output.token_type,
            "role": output.role,
        }
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error


@app.get("/api/v1/auth/verify")
def verify_token(authorization: str | None = Header(default=None)):
    token = _extract_bearer_token(authorization)
    try:
        claims = _token_service.decode_token(token)
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


@app.get("/api/v1/auth/authorize")
def authorize(required_role: str, authorization: str | None = Header(default=None)):
    token = _extract_bearer_token(authorization)
    try:
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
