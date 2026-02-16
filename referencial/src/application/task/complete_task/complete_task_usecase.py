from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.task.task_repository_interface import TaskRepositoryInterface
from application.task.complete_task.complete_task_dto import (
    CompleteTaskInputDto,
    CompleteTaskOutputDto,
)


class CompleteTaskUseCase(UseCaseInterface):

    def __init__(self, task_repository: TaskRepositoryInterface):
        self.task_repository = task_repository

    def execute(self, input: CompleteTaskInputDto) -> CompleteTaskOutputDto:

        task = self.task_repository.find_task(task_id=input.id)

        task.mark_as_completed()

        self.task_repository.update_task(task=task)

        return CompleteTaskOutputDto(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
        )
