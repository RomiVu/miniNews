from typing import List
from datetime import datetime

from pydantic import BaseModel, ValidationError, validator, Field

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None

class User(BaseModel):
    username: str

    class Config:
        orm_mode = True

class UserIn(User):
    password: str

class UserInDB(User):
    email: str = ''
    phone:str = Field(None, example="18667891234")
    vaild_before: datetime
    last_seen: datetime
    password_hash: str

class UserDetail(User):
    email: str = Field(None, example="hello@gmail.com")
    phone: str = Field(None, example="18667891234")
    vaild_before: datetime
    last_seen: datetime

# class Application(BaseModel):
#     id: int
#     name: str
#     description: str

#     clients: List[Client]

# class Client(BaseModel):
#     id: int
#     organization: str
#     address: str
#     remark: str

#     staff: List[User]
#     apps: List[Application]

# class Task(BaseModel):
#     id: int
#     url: str
#     user_id: int
#     modify_time: datetime
#     priority: int
#     description: str
#     schedule_time: datetime
#     interval: int

#     users: List[User]
#     task_type: List[TaskType]


# class TaskType(BaseModel):
#     id: int
#     name: str
#     description: str

#     tasks: List[Task]

# class Permission(BaseModel):
#     id: int
#     name: str
#     description: str

#     roles: List[Role]

# class Role(BaseModel):
#     id: int
#     name: str
#     description: str

#     permissions: List[Permission]
#     users: List[User]
