import datetime, enum
from typing import Annotated
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime,  mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        # Вместо выполнения функции Python, мы говорим SQLAlchemy
        # отправить SQL-команду на сторону базы
        onupdate=text("TIMEZONE('utc', now())")
)]

class UsersModel(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str | None]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    role: Mapped[str] = mapped_column(default="user")

    tasks: Mapped[list["TasksModel"]] = relationship("TasksModel", back_populates="user")

class PriorityEnum(enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

class TasksModel(Base):
    __tablename__ = "tasks"

    id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[str | None]
    priority: Mapped[PriorityEnum]
    is_completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped["UsersModel"] = relationship("UsersModel", back_populates="tasks")