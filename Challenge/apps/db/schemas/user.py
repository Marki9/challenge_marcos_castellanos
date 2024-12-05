from pydantic import Field, ConfigDict, BaseModel, EmailStr
from typing import List, Optional

from apps.db.schemas.customResponse import CustomResponse
from typing_extensions import Annotated


class Post(BaseModel):
    title: str
    content: str
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str
    age: Annotated[int, Field(ge=18)]
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id:int
    posts: List["Post"] = []
    model_config = ConfigDict(from_attributes=True)


class UserResponse(CustomResponse):
    data: Optional[List[User]] = None
