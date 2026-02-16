from typing import List
from uuid import UUID
from domain.task.task_entity import Task
from domain.task.task_repository_interface import TaskRepositoryInterface
from sqlalchemy.orm.session import Session

from infra.task.sqlalchemy.task_model import TaskModel


class TaskRepository(TaskRepositoryInterface):

    def __init__(self, session: Session):
        self.session: Session = session

    def register_task(self, task: Task) -> None:

        try:
            task_model = TaskModel(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
            )

            self.session.add(task_model)
            self.session.commit()
        except:
            raise Exception("error to register task in database.")

        return None

    def find_task(self, task_id: UUID) -> Task:

        task_in_db = self.session.query(TaskModel).filter_by(id=task_id).first()

        if task_in_db is None:
            raise Exception(f"task with id {task_id} does not exist.")

        return Task(
            id=task_in_db.id,
            user_id=task_in_db.user_id,
            title=task_in_db.title,
            description=task_in_db.description,
            completed=task_in_db.completed,
        )

    def list_tasks_from_user(self, user_id: UUID) -> List[Task]:

        tasks_from_user_in_db = (
            self.session.query(TaskModel).filter(TaskModel.user_id == user_id).all()
        )

        tasks = []

        for task_from_user_in_db in tasks_from_user_in_db:
            tasks.append(
                Task(
                    id=task_from_user_in_db.id,
                    user_id=task_from_user_in_db.user_id,
                    title=task_from_user_in_db.title,
                    description=task_from_user_in_db.description,
                    completed=task_from_user_in_db.completed,
                )
            )

        return tasks

    def update_task(self, task: Task) -> None:

        try:
            self.session.query(TaskModel).filter(TaskModel.id == task.id).update(
                {
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                }
            )
            self.session.commit()
        except:
            raise Exception("error to update task in database.")

        return None

    def delete_task(self, task_id: UUID) -> None:

        try:
            self.session.query(TaskModel).filter(TaskModel.id == task_id).delete(
                synchronize_session=False
            )
            self.session.commit()
        except:
            raise Exception(f"error to delete task {task_id}")

        return None
