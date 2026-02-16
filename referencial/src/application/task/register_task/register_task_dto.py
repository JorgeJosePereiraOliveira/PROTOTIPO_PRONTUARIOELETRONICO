from pydantic import BaseModel
from uuid import UUID


class RegisterTaskInputDto(BaseModel):
    user_id: UUID
    title: str
    description: str


class RegisterTaskOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str
    completed: bool
