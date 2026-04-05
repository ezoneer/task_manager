from pydantic import BaseModel, ConfigDict

class UserAddDTO(BaseModel):
    username: str

class UserDTO(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
