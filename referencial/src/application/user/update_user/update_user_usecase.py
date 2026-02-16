from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.user.user_repository_interface import UserRepositoryInterface
from application.user.update_user.update_user_dto import (
    UpdateUserInputDto,
    UpdateUserOutputDto,
)
from domain.user.user_entity import User
import uuid


class UpdateUserUseCase(UseCaseInterface):

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, input: UpdateUserInputDto) -> UpdateUserOutputDto:

        user = User(id=uuid.uuid4(), name=input.name)

        self.user_repository.update_user(user=user)

        return UpdateUserOutputDto(id=user.id, name=user.name)
