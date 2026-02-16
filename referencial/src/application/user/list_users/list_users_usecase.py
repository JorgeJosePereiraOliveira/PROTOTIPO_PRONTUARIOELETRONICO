from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.user.user_repository_interface import UserRepositoryInterface
from application.user.list_users.list_users_dto import (
    ListUsersInputDto,
    ListUsersOutputDto,
    UserDto,
)


class ListUsersUseCase(UseCaseInterface):

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, input: ListUsersInputDto) -> ListUsersOutputDto:

        users = self.user_repository.list_users()

        output = []

        for user in users:
            output.append(UserDto(id=user.id, name=user.name))

        return ListUsersOutputDto(users=output)
