from typing import List, Optional
from schemas.user_schemas import UserDTO
from schemas.task_schemas import TaskDTO

class UserRelDTO(UserDTO):
    tasks: List[TaskDTO] = []

class TaskRelDTO(TaskDTO):
    user: Optional[UserDTO] = None