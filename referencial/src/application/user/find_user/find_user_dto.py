from pydantic import BaseModel
from uuid import UUID
from typing import List


class FindUserInputDto(BaseModel):
    id: UUID


class TaskOutputDto(BaseModel):
    id: UUID
    title: str
    description: str
    completed: bool


class FindUserOutputDto(BaseModel):
    id: UUID
    name: str
    tasks: List[TaskOutputDto]
    pending_tasks: int
