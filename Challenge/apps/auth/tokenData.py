from pydantic import BaseModel
from typing import List


class TokenData(BaseModel):
    username: str  # | None = None
    scopes: List[str] = []
