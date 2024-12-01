from pydantic import BaseModel, constr
from typing import List, Optional

class Post(BaseModel):
    title: constr(max_length=50)
    owner_id: int

class TagBase(BaseModel):
    text: constr(max_length=50)

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    posts: List[Post] = []

    class Config:
        orm_mode = True