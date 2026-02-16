from pydantic import BaseModel
from uuid import UUID


class DeleteTaskInputDto(BaseModel):
    id: UUID


class DeleteTaskOutputDto(BaseModel):
    message: str
