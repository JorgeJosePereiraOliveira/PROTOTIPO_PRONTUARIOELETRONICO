from pydantic import BaseModel
from uuid import UUID
from typing import List


class ListUsersInputDto(BaseModel):
    pass


class UserDto(BaseModel):
    id: UUID
    name: str


class ListUsersOutputDto(BaseModel):
    users: List[UserDto]
