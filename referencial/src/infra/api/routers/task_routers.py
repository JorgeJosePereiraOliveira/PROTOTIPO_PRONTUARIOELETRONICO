from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from infra.api.database import get_session
from sqlalchemy.orm import Session

from infra.task.sqlalchemy.task_repository import TaskRepository
from application.task.complete_task.complete_task_dto import CompleteTaskInputDto
from application.task.complete_task.complete_task_usecase import CompleteTaskUseCase
from application.task.delete_task.delete_task_dto import DeleteTaskInputDto
from application.task.delete_task.delete_task_usecase import DeleteTaskUseCase
from application.task.find_task.find_task_dto import FindTaskInputDto
from application.task.find_task.find_task_usecase import FindTaskUseCase
from application.task.register_task.register_task_dto import RegisterTaskInputDto
from application.task.register_task.register_task_usecase import RegisterTaskUseCase
from infra.api.presenters.task_presenter import TaskPresenter


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
def register_task(
    request: RegisterTaskInputDto, session: Session = Depends(get_session)
):
    try:
        task_repository = TaskRepository(session=session)
        usecase = RegisterTaskUseCase(task_repository=task_repository)
        output = usecase.execute(input=request)
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{task_id}")
def find_task(task_id: UUID, session: Session = Depends(get_session)):
    try:
        task_repository = TaskRepository(session=session)
        usecase = FindTaskUseCase(task_repository=task_repository)
        output = usecase.execute(input=FindTaskInputDto(id=task_id))

        output_xml = TaskPresenter.toXML(output)
        output_json = TaskPresenter.toJSON(output)

        return {"json": output_json, "xml": output_xml}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{task_id}")
def complete_task(task_id: UUID, session: Session = Depends(get_session)):
    try:
        task_repository = TaskRepository(session=session)
        usecase = CompleteTaskUseCase(task_repository=task_repository)
        output = usecase.execute(input=CompleteTaskInputDto(id=task_id))
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{task_id}")
def delete_task(task_id: UUID, session: Session = Depends(get_session)):
    try:
        task_repository = TaskRepository(session=session)
        usecase = DeleteTaskUseCase(task_repository=task_repository)
        output = usecase.execute(input=DeleteTaskInputDto(id=task_id))
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
