from pydantic import BaseModel
from typing import List, TypeVar, Generic, Optional

# Definimos un tipo genérico para poder usarlo en CustomResponse


class CustomResponse(BaseModel):
    data: Optional[List[BaseModel]]
    success: bool
    count: int
    message: str

    class configDict:
        orm_mode = True

    @classmethod
    def create(cls, data: List[BaseModel], success: bool, success_message: str = "Operación realizada correctamente", failure_message: str = "Operación fallida") -> "CustomResponse[T]":
        if success:
            return cls(
                data=data,
                success=True,
                count=len(data),
                message=success_message
            )
        else:
            return cls(
                data=[],
                success=False,
                count=0,
                message=failure_message
            )
