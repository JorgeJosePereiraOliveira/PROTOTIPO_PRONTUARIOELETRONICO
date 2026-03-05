from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.auth.application.auth.authenticate_user_usecase import (
    AuthenticateUserInputDTO,
    AuthenticateUserUseCase,
)
from src.auth.application.auth.authorize_role_usecase import (
    AuthorizeRoleInputDTO,
    AuthorizeRoleUseCase,
)
from src.auth.infra.auth.jwt_token_service import JwtTokenService
from src.auth.infra.auth.bcrypt_password_hasher import BcryptPasswordHasher
from src.auth.infra.auth.sqlalchemy_refresh_token_repository import (
    SqlAlchemyRefreshTokenRepository,
)
from src.auth.infra.auth.sqlalchemy_base import Base
from src.auth.infra.auth.sqlalchemy_models import UserModel
from src.auth.infra.auth.sqlalchemy_user_repository import SqlAlchemyUserRepository


def _build_sqlalchemy_repositories() -> tuple[SqlAlchemyUserRepository, SqlAlchemyRefreshTokenRepository]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = session_factory()

    hasher = BcryptPasswordHasher()
    session.add_all(
        [
            UserModel(
                id="u-admin",
                username="admin",
                password_hash=hasher.hash("admin123"),
                role="admin",
                active=True,
            ),
            UserModel(
                id="u-prof",
                username="profissional",
                password_hash=hasher.hash("prof123"),
                role="profissional",
                active=True,
            ),
        ]
    )
    session.commit()
    return SqlAlchemyUserRepository(session), SqlAlchemyRefreshTokenRepository(session)


def test_authenticate_user_success():
    repository, refresh_repository = _build_sqlalchemy_repositories()
    hasher = BcryptPasswordHasher()
    token_service = JwtTokenService(secret_key="test-secret")
    use_case = AuthenticateUserUseCase(
        repository,
        hasher,
        token_service,
        refresh_repository,
    )

    output = use_case.execute(
        AuthenticateUserInputDTO(username="admin", password="admin123")
    )

    assert output.access_token
    assert output.token_type == "bearer"
    assert output.role == "admin"


def test_authenticate_user_invalid_credentials():
    repository, refresh_repository = _build_sqlalchemy_repositories()
    hasher = BcryptPasswordHasher()
    token_service = JwtTokenService(secret_key="test-secret")
    use_case = AuthenticateUserUseCase(
        repository,
        hasher,
        token_service,
        refresh_repository,
    )

    try:
        use_case.execute(
            AuthenticateUserInputDTO(username="admin", password="wrong-password")
        )
        assert False, "expected ValueError"
    except ValueError as error:
        assert "invalid credentials" in str(error)


def test_authorize_role_admin_can_access_professional_resource():
    token_service = JwtTokenService(secret_key="test-secret")
    use_case = AuthorizeRoleUseCase(token_service)

    token = token_service.create_access_token(
        user_id="u-admin",
        username="admin",
        role="admin",
    )

    output = use_case.execute(
        AuthorizeRoleInputDTO(token=token, required_role="profissional")
    )

    assert output.authorized is True
    assert output.role == "admin"
