from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from infra.api.database import get_session
from sqlalchemy.orm import Session

from infra.task.sqlalchemy.task_repository import TaskRepository
from infra.user.sqlalchemy.user_repository import UserRepository
from application.user.add_user.add_user_dto import AddUserInputDto
from application.user.add_user.add_user_usecase import AddUserUseCase
from application.user.find_user.find_user_dto import FindUserInputDto
from application.user.find_user.find_user_usecase import FindUserUseCase
from application.user.list_users.list_users_dto import ListUsersInputDto
from application.user.list_users.list_users_usecase import ListUsersUseCase

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def add_user(request: AddUserInputDto, session: Session = Depends(get_session)):
    try:
        user_repository = UserRepository(session=session)
        usecase = AddUserUseCase(user_repository=user_repository)
        output = usecase.execute(input=request)
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{user_id}")
def find_user(user_id: UUID, session: Session = Depends(get_session)):
    try:
        user_repository = UserRepository(session=session)
        task_repository = TaskRepository(session=session)
        usecase = FindUserUseCase(
            user_repository=user_repository, task_repository=task_repository
        )
        output = usecase.execute(input=FindUserInputDto(id=user_id))
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_users(session: Session = Depends(get_session)):
    try:
        user_repository = UserRepository(session=session)
        usecase = ListUsersUseCase(user_repository=user_repository)
        output = usecase.execute(input=ListUsersInputDto())
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
