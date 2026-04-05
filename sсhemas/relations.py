from typing import List, Optional
from sсhemas.user_schemas import UserDTO
from sсhemas.task_schemas import TaskDTO

class UserRelDTO(UserDTO):
    tasks: List[TaskDTO] = []

class TaskRelDTO(TaskDTO):
    user: Optional[UserDTO] = None