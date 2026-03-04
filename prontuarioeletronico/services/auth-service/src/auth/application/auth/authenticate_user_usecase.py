from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.auth.user_repository_interface import UserRepositoryInterface
from .contracts import PasswordHasher, TokenService


@dataclass
class AuthenticateUserInputDTO:
    username: str
    password: str


@dataclass
class AuthenticateUserOutputDTO:
    access_token: str
    token_type: str
    role: str


class AuthenticateUserUseCase(UseCase[AuthenticateUserInputDTO, AuthenticateUserOutputDTO]):
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._token_service = token_service

    def execute(self, input_dto: AuthenticateUserInputDTO) -> AuthenticateUserOutputDTO:
        if not input_dto.username or not input_dto.password:
            raise ValueError("username and password are required")

        user = self._user_repository.find_by_username(input_dto.username)
        if user is None or not user.active:
            raise ValueError("invalid credentials")

        is_valid_password = self._password_hasher.verify(
            input_dto.password,
            user.password_hash,
        )
        if not is_valid_password:
            raise ValueError("invalid credentials")

        access_token = self._token_service.create_access_token(
            user_id=user.id,
            username=user.username,
            role=user.role.value,
        )

        return AuthenticateUserOutputDTO(
            access_token=access_token,
            token_type="bearer",
            role=user.role.value,
        )
