from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.task.task_repository_interface import TaskRepositoryInterface
from application.task.register_task.register_task_dto import (
    RegisterTaskInputDto,
    RegisterTaskOutputDto,
)
from domain.task.task_entity import Task
from uuid import uuid4


class RegisterTaskUseCase(UseCaseInterface):

    def __init__(self, task_repository: TaskRepositoryInterface):
        self.task_repository = task_repository

    def execute(self, input: RegisterTaskInputDto) -> RegisterTaskOutputDto:

        task = Task(
            id=uuid4(),
            user_id=input.user_id,
            title=input.title,
            description=input.description,
            completed=False,
        )

        self.task_repository.register_task(task=task)

        return RegisterTaskOutputDto(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
        )
