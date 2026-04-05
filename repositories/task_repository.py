from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from models import TasksModel
from sqlalchemy import select, update, delete


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_task(self, task_data: dict) -> TasksModel:
        new_task = TasksModel(**task_data)

        self.session.add(new_task)
        await self.session.commit()

        await self.session.refresh(new_task) #refresh подтягивает данные, которые база создала сама(например id)
        return new_task

    async def get_all_tasks(self, user_id: int) -> Sequence[TasksModel]:
        query = select(TasksModel).filter_by(user_id=user_id)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def update_task(self, task_id: int, user_id: int, data: dict):
        query = (
            update(TasksModel)
            .filter_by(id=task_id, user_id=user_id)
            .values(**data)
            .returning(TasksModel)
        )

        result = await self.session.execute(query)
        await self.session.commit()

        return result.scalar_one_or_none()

    async def delete_task(self, task_id: int, user_id: int) -> int | None:
        query = (delete(TasksModel)
                 .filter_by(id=task_id, user_id=user_id)
                 .returning(TasksModel.id))
        result = await self.session.execute(query)
        await self.session.commit()

        return result.scalar_one_or_none()
