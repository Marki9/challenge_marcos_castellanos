from pydantic import BaseModel, constr
from typing import List, Optional

from apps.db.schemas.customResponse import CustomResponse


class Tag(BaseModel):
    text: constr(max_length=50)
    
class PostBase(BaseModel):
    title: constr(max_length=20)
    content: str
    tags: List[Tag]

class PostCreate(PostBase):
    pass

class PostResponse(CustomResponse):
    data: Optional[List[PostBase]]


    class ConfigDict:
        orm_mode = True