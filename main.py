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
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(ProcessTimeMiddleware)
app.include_router(users_router)
app.include_router(tasks_router)

UserRepoDep = Annotated[UsersRepository, Depends()]

origins = [
    "http://localhost:63342",
    "http://127.0.0.1:63342",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    print("Запуск сервера на http://localhost:8080")
    uvicorn.run(app, host="localhost", port=8080)