from typing import Annotated
import uvicorn
from contextlib import asynccontextmanager
from middlewares import ProcessTimeMiddleware
from fastapi import FastAPI, Depends
from database import async_engine
from models import Base
from repositories.user_repository import UsersRepository
from routes.tasks import router as tasks_router
from routes.users import router as users_router
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(ProcessTimeMiddleware)
app.include_router(users_router)
app.include_router(tasks_router, dependencies=[Depends(oauth2_scheme)])


UserRepoDep = Annotated[UsersRepository, Depends()]

if __name__ == '__main__':
    print("Запуск сервера на http://127.0.0.1:8080")
    uvicorn.run(app, host="127.0.0.1", port=8080)