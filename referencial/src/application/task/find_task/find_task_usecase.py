from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.task.task_repository_interface import TaskRepositoryInterface
from application.task.find_task.find_task_dto import FindTaskInputDto, FindTaskOutputDto


class FindTaskUseCase(UseCaseInterface):

    def __init__(self, task_repository: TaskRepositoryInterface):
        self.task_repository = task_repository

    def execute(self, input: FindTaskInputDto) -> FindTaskOutputDto:

        task = self.task_repository.find_task(task_id=input.id)

        return FindTaskOutputDto(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
        )
