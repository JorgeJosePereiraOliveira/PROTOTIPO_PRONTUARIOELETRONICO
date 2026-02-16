from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.user.user_repository_interface import UserRepositoryInterface
from domain.task.task_repository_interface import TaskRepositoryInterface
from application.user.find_user.find_user_dto import (
    FindUserInputDto,
    FindUserOutputDto,
    TaskOutputDto,
)


class FindUserUseCase(UseCaseInterface):

    user_repository: UserRepositoryInterface
    task_repository: TaskRepositoryInterface

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        task_repository: TaskRepositoryInterface,
    ):
        self.user_repository = user_repository
        self.task_repository = task_repository

    def execute(self, input: FindUserInputDto) -> FindUserOutputDto:

        user = self.user_repository.find_user(user_id=input.id)

        tasks_from_user = self.task_repository.list_tasks_from_user(user_id=user.id)

        user.collect_tasks(tasks=tasks_from_user)

        tasks_output = []

        for task in user.tasks:
            tasks_output.append(
                TaskOutputDto(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                )
            )

        return FindUserOutputDto(
            id=user.id,
            name=user.name,
            tasks=tasks_output,
            pending_tasks=user.count_pending_tasks(),
        )
