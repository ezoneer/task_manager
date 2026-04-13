from typing import Annotated

import jwt
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from passlib.context import CryptContext
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from config import settings
from pydantic import EmailStr

from repositories.user_repository import UsersRepository
from schemas.schemas import SUserRegister

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class AuthService:
    def __init__ (self, user_repo: UsersRepository, response: Response):
        self.user_repo = user_repo
        self.response = response

    async def register_new_user(self, user_data:SUserRegister):
        existing_user = await self.user_repo.get_user_by_email(email=str(user_data.email))

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Пользователь уже существует'
            )

        user_dict = user_data.model_dump()
        user_dict["password"] = get_password_hash(user_data.password)

        return await self.user_repo.add_user(user_dict)

    async def authenticate_user(self, email: str | EmailStr, password: str):
        user = await self.user_repo.get_user_by_email(email=str(email))

        if not user or not verify_password(password, str(user.password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Неверная почта или пароль'
            )

        return self.create_tokens(user_id=int(user.id), role=str(user.role))

    @staticmethod
    def create_tokens(user_id: int, role: str):
        base_payload = {
            'sub': str(user_id),
            'role': role,
            'iat': datetime.now(timezone.utc),
        }
        access_token = jwt.encode(
            {**base_payload, 'type': 'access', 'exp': datetime.now(timezone.utc) + timedelta(minutes=30)},
            settings.JWT_SECRET, algorithm=settings.ALGORITHM
        )
        refresh_token = jwt.encode(
            {**base_payload, 'type': 'refresh', 'exp': datetime.now(timezone.utc) + timedelta(days=30)},
            settings.JWT_SECRET, algorithm=settings.ALGORITHM
        )
        return {"access_token": access_token, "refresh_token": refresh_token}

