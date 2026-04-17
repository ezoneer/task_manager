from fastapi import APIRouter, Depends, Response
from typing import Annotated

from dependencies import get_current_user
from models import UsersModel
from services.auth_service import AuthService
from schemas.schemas import SUserRegister, SUserAuth
from repositories.user_repository import UsersRepository

router = APIRouter(prefix='/auth', tags=['Auth'])

async def get_auth_service(response: Response, repo: Annotated[UsersRepository, Depends()]) -> AuthService:
    return AuthService(user_repo=repo, response=response)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/register")
async def register_user(
    user_data: SUserRegister,
    auth_service: AuthServiceDep
):
    return await auth_service.register_new_user(user_data=user_data)


@router.post("/login")
async def login(
    response: Response,
    auth_service: AuthServiceDep,
    user_data: SUserAuth
):

    tokens = await auth_service.authenticate_user(
        email=user_data.email,
        password=user_data.password
    )

    response.set_cookie(key="users_access_token", value=tokens["access_token"], httponly=True)
    response.set_cookie(key="users_refresh_token", value=tokens["refresh_token"], httponly=True, path="/auth/refresh")

    return {"message": "Аутентификация пройдена успешно!"}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    response.delete_cookie(key="users_refresh_token", path="/auth/refresh")

    return {"message": "Сессия окончена"}

@router.get("/me")
async def get_me(user: UsersModel = Depends(get_current_user)):
    return user