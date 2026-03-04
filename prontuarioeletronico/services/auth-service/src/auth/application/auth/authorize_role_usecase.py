from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.auth.role import Role
from .contracts import TokenService


@dataclass
class AuthorizeRoleInputDTO:
    token: str
    required_role: str


@dataclass
class AuthorizeRoleOutputDTO:
    authorized: bool
    role: str


class AuthorizeRoleUseCase(UseCase[AuthorizeRoleInputDTO, AuthorizeRoleOutputDTO]):
    def __init__(self, token_service: TokenService):
        self._token_service = token_service

    def execute(self, input_dto: AuthorizeRoleInputDTO) -> AuthorizeRoleOutputDTO:
        if not input_dto.token:
            raise ValueError("token is required")
        if not input_dto.required_role:
            raise ValueError("required_role is required")

        claims = self._token_service.decode_token(input_dto.token)
        role = claims.get("role")

        authorized = role == input_dto.required_role or role == Role.ADMIN.value

        return AuthorizeRoleOutputDTO(
            authorized=authorized,
            role=role,
        )
