from pydantic import BaseModel, ConfigDict
from typing import List, TypeVar, Generic, Optional

# Definimos un tipo genérico para poder usarlo en CustomResponse


class CustomResponse(BaseModel):
    data: List[BaseModel]
    success: bool
    count: int
    message: str
    model_config = ConfigDict(from_attributes=True)

