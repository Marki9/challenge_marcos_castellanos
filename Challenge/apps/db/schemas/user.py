from pydantic import BaseModel,EmailStr,conint
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    age:conint(ge=18)  # La edad debe ser un entero mayor o igual a 18
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    posts: List["Post"] = []
    
class UserResponse(UserBase):
    List[UserBase]    

    class Config:
        orm_mode = True