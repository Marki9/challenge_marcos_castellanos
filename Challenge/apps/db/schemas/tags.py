from pydantic import BaseModel, constr
from typing import List, Optional

from apps.db.schemas.customResponse import CustomResponse


class Post(BaseModel):
    title: constr(max_length=50)
    owner_id: int


class TagBase(BaseModel):
    text: constr(max_length=50)


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    posts: List[Post] = []


class TagResponse(CustomResponse):
    data: Optional[List[Tag]]


