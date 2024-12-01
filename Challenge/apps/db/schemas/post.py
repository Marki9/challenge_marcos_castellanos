from pydantic import BaseModel, constr
from typing import List, Optional

class Tag(BaseModel):
    text: constr(max_length=50)
    
class PostBase(BaseModel):
    title: constr(max_length=20)
    owner_id: int

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    tags: List[Tag] = []

    class Config:
        orm_mode = True