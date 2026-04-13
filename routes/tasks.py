from typing import Annotated
from fastapi import APIRouter, Depends
from database import DatabaseStorageDep
from dependencies import get_current_user
from models import UsersModel
from schemas.task_schemas import TaskAddDTO, TaskUpdateDTO
from services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/add")
async def add_task_handler(
        task: TaskAddDTO,
        db: DatabaseStorageDep,
        current_user: Annotated[UsersModel, Depends(get_current_user)]
):
    service = TaskService(db)
    return await service.add_task(task, user_id = current_user.id)


@router.get("/all")
async def get_tasks_handler(
    current_user: Annotated[UsersModel, Depends(get_current_user)],
    db: DatabaseStorageDep
):
    service = TaskService(db)
    return await service.get_all_tasks(user_id=current_user.id)


@router.put("/{task_id}")
async def updated_task(
    task_id: int,
    current_user: Annotated[UsersModel, Depends(get_current_user)],
    data: TaskUpdateDTO,
    db: DatabaseStorageDep
):
    service = TaskService(db)
    return await service.update_task(task_id, user_id=current_user.id, task_data= data)


@router.delete("/delete/{task_id}")
async def deleted_task(
        task_id: int,
        current_user: Annotated[UsersModel, Depends(get_current_user)],
        db: DatabaseStorageDep):
    service = TaskService(db)
    return await service.delete_task(task_id, user_id=current_user.id)
