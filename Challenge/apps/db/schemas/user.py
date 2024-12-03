from pydantic import BaseModel, EmailStr, conint
from typing import List, Optional

from apps.db.schemas.customResponse import CustomResponse


class Post(BaseModel):
    title: str
    content: str


class UserBase(BaseModel):
    username: str
    age: conint(ge=18)  # La edad debe ser un entero mayor o igual a 18
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id:int
    posts: List["Post"] = []


class UserResponse(CustomResponse):
    data: Optional[List[User]]
