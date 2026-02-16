from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.user.user_repository_interface import UserRepositoryInterface
from application.user.add_user.add_user_dto import AddUserInputDto, AddUserOutputDto
from domain.user.user_entity import User
import uuid


class AddUserUseCase(UseCaseInterface):

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, input: AddUserInputDto) -> AddUserOutputDto:

        user = User(id=uuid.uuid4(), name=input.name)

        self.user_repository.add_user(user=user)

        return AddUserOutputDto(id=user.id, name=user.name)
