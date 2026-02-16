from pydantic import BaseModel
from uuid import UUID


class AddUserInputDto(BaseModel):
    name: str


class AddUserOutputDto(BaseModel):
    id: UUID
    name: str
