from pydantic import BaseModel, EmailStr, Field

class SUserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Пароль, минимум 6 символов")

class SUserAuth(BaseModel):
    email: EmailStr
    password: str

class UserAddDTO(BaseModel):
    username: str