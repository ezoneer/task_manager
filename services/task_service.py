from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from repositories.task_repository import TaskRepository
from repositories.user_repository import UsersRepository
from sсhemas.task_schemas import TaskUpdateDTO, TaskAddDTO


class TaskService:
    def __init__(self, session : AsyncSession):
        self.task_repo = TaskRepository(session)
        self.user_repo = UsersRepository(session)


    async def add_task(self, task:TaskAddDTO, user_id: int):
        exists = await self.user_repo.check_user_exists(user_id)
        if not exists:
            raise HTTPException(status_code=404, detail="Юзер не найден")

        task_data = task.model_dump()

        task_data["user_id"] = user_id
        new_task = await self.task_repo.add_task(task_data)

        return {"status": "success", "data": new_task}

    async def get_all_tasks(self, user_id: int):
        tasks = await self.task_repo.get_all_tasks(user_id)
        return tasks

    async def update_task(self, task_id: int, user_id: int, task_data: TaskUpdateDTO):
        update_dict = task_data.model_dump(exclude_unset=True)

        if not update_dict:
            return {"message": "Нет данных для обновления"}

        updated_task = await self.task_repo.update_task(task_id, user_id, update_dict)

        if not updated_task:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        return await self.task_repo.update_task(task_id, user_id, update_dict)

    async def delete_task(self, task_id: int, user_id: int):
        deleted_id = await self.task_repo.delete_task(task_id, user_id)

        if deleted_id is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        return {"status": "success", "message": f"Задача с {task_id} удалена"}


