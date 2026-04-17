from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config import settings

from fastapi import Depends
from typing import Annotated, AsyncGenerator

async_engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    echo=True
)

class DatabaseStorage:
    def __init__(self, session=None):
        if session is None:
            self.session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
        else:
            self.session = session

    async def __call__(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session() as session:
            yield session


database_storage = DatabaseStorage()
DatabaseStorageDep = Annotated[AsyncSession, Depends(database_storage)]


class Base(DeclarativeBase):
    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append (f"{col} = {getattr(self, col)}")
        return f"<{self.__class__.__name__} {','. join(cols)}>"
