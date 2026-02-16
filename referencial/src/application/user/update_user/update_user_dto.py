from pydantic import BaseModel
from uuid import UUID


class UpdateUserInputDto(BaseModel):
    id: UUID
    name: str


class UpdateUserOutputDto(BaseModel):
    id: UUID
    name: str
