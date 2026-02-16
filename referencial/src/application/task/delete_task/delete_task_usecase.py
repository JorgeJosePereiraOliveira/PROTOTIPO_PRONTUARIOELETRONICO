from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.task.task_repository_interface import TaskRepositoryInterface
from application.task.delete_task.delete_task_dto import (
    DeleteTaskInputDto,
    DeleteTaskOutputDto,
)


class DeleteTaskUseCase(UseCaseInterface):

    def __init__(self, task_repository: TaskRepositoryInterface):
        self.task_repository = task_repository

    def execute(self, input: DeleteTaskInputDto) -> DeleteTaskOutputDto:

        self.task_repository.delete_task(task_id=input.id)

        return DeleteTaskOutputDto(
            message=f"task with id {input.id} deleted successfully."
        )
