from typing import List, Optional
from user_schemas import UserDTO
from task_schemas import TaskDTO

class UserRelDTO(UserDTO):
    tasks: List[TaskDTO] = []

class TaskRelDTO(TaskDTO):
    user: Optional[UserDTO] = None