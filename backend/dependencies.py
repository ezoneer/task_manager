from fastapi import Request, HTTPException, status, Depends
import jwt

from backend.config import settings
from backend.database import DatabaseStorageDep
from backend.repositories.user_repository import UsersRepository


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Вы не авторизованы")
    return token


async def get_current_user(
    db: DatabaseStorageDep,
    token: str = Depends(get_token),
):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM]
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен невалиден")

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    repo = UsersRepository(db)
    user = await repo.get_user_by_id(int(user_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user


def decode_token(token: str):
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.ALGORITHM]
    )
    return payload