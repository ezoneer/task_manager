from database import DatabaseStorageDep
from models import UsersModel
from sqlalchemy import select

class UsersRepository:
    def __init__(self, db: DatabaseStorageDep):
        self.session = db

    async def add_user(self, user_data: dict) -> UsersModel:
        new_user = UsersModel(**user_data)

        self.session.add(new_user)
        await self.session.commit()

        await self.session.refresh(new_user)
        return new_user


    async def get_user_by_id(self, user_id: int) -> UsersModel | None:
        return await self.session.get(UsersModel, user_id)

    async def get_user_by_email(self, email: str) -> UsersModel | None:
        query = select(UsersModel).filter_by(email=email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def check_user_exists(self, user_id: int) -> bool:
        user = await self.session.get(UsersModel, user_id)

        return user is not None