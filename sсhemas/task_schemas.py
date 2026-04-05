from pydantic import BaseModel, ConfigDict, Field
from models import PriorityEnum
from datetime import datetime
from typing import Optional

class TaskAddDTO(BaseModel):
    title: str = Field(min_length=1, max_length=50, description="Название задачи")
    description: Optional[str] = Field(None, max_length=500, description="Описание задачи")
    priority: PriorityEnum = PriorityEnum.medium


class TaskDTO(TaskAddDTO):
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskUpdateDTO(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[PriorityEnum] = None
    is_completed: Optional[bool] = None