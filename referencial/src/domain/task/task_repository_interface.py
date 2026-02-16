from abc import ABC, abstractmethod
from domain.task.task_entity import Task
from typing import List
from uuid import UUID


class TaskRepositoryInterface(ABC):

    @abstractmethod
    def register_task(self, task: Task) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_task(self, task_id: UUID) -> Task:
        raise NotImplementedError

    @abstractmethod
    def list_tasks_from_user(self, user_id: UUID) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def update_task(self, task: Task) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, task_id: UUID) -> None:
        raise NotImplementedError
