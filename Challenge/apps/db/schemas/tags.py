from pydantic import StringConstraints, BaseModel, ConfigDict
from typing import List, Optional

from apps.db.schemas.customResponse import CustomResponse
from typing_extensions import Annotated


class Post(BaseModel):
    title: Annotated[str, StringConstraints(max_length=50)]
    content:str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class TagBase(BaseModel):
    text: Annotated[str, StringConstraints(max_length=50)]
    posts: List[Post] = []


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id:int

    model_config = ConfigDict(from_attributes=True)


class TagResponse(CustomResponse):
    data: Optional[List[Tag]] = None
