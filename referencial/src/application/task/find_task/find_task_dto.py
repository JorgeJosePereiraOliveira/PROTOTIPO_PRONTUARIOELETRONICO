from pydantic import BaseModel
from uuid import UUID


class FindTaskInputDto(BaseModel):
    id: UUID


class FindTaskOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str
    completed: bool
