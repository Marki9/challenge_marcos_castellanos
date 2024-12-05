from pydantic import StringConstraints, BaseModel, ConfigDict
from typing import List, Optional

from apps.db.schemas.customResponse import CustomResponse
from typing_extensions import Annotated


class Tag(BaseModel):
    text: Annotated[str, StringConstraints(max_length=50)]
    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    title: Annotated[str, StringConstraints(max_length=20)]
    content: str
    tags: List[Tag]


class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    title: Annotated[str, StringConstraints(max_length=20)]
    content: str
    tags: List[Tag]
    model_config = ConfigDict(from_attributes=True)


class PostResponse(CustomResponse):
    data: Optional[List[Post]] = None
