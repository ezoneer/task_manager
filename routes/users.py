from fastapi import APIRouter, Depends, Response
from typing import Annotated

from dependencies import get_current_user
from models import UsersModel
from services.auth_service import AuthService
from sсhemas.schemas import SUserRegister
from repositories.user_repository import UsersRepository
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/auth', tags=['Auth'])

async def get_auth_service(response: Response, repo: Annotated[UsersRepository, Depends()]) -> AuthService:
    return AuthService(user_repo=repo, response=response)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/register/")
async def register_user(user_data: SUserRegister, auth_service: AuthServiceDep):
    return await auth_service.register_new_user(user_data=user_data)

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
async def login(
    auth_service: AuthServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    return await auth_service.authenticate_user(
        email=form_data.username,
        password=form_data.password
    )

@router.post("/logout")
async def logout_user(auth_service: AuthServiceDep):
    return auth_service.logout_user()

@router.get("/me")
async def get_me(user: UsersModel = Depends(get_current_user)):
    return user
