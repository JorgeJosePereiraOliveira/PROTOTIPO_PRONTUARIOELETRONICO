from pydantic import BaseModel
from uuid import UUID


class CompleteTaskInputDto(BaseModel):
    id: UUID


class CompleteTaskOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str
    completed: bool
