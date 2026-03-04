from src.auth.application.auth.authenticate_user_usecase import (
    AuthenticateUserInputDTO,
    AuthenticateUserUseCase,
)
from src.auth.application.auth.authorize_role_usecase import (
    AuthorizeRoleInputDTO,
    AuthorizeRoleUseCase,
)
from src.auth.infra.auth.in_memory_user_repository import InMemoryUserRepository
from src.auth.infra.auth.jwt_token_service import JwtTokenService
from src.auth.infra.auth.sha256_password_hasher import Sha256PasswordHasher


def test_authenticate_user_success():
    repository = InMemoryUserRepository()
    hasher = Sha256PasswordHasher()
    token_service = JwtTokenService(secret_key="test-secret")
    use_case = AuthenticateUserUseCase(repository, hasher, token_service)

    output = use_case.execute(
        AuthenticateUserInputDTO(username="admin", password="admin123")
    )

    assert output.access_token
    assert output.token_type == "bearer"
    assert output.role == "admin"


def test_authenticate_user_invalid_credentials():
    repository = InMemoryUserRepository()
    hasher = Sha256PasswordHasher()
    token_service = JwtTokenService(secret_key="test-secret")
    use_case = AuthenticateUserUseCase(repository, hasher, token_service)

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
