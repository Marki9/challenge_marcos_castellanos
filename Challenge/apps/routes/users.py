import hashlib
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from apps.config import logger
from apps.db.db import get_db
from apps.db.schemas.user import UserResponse, UserBase
from apps.db.models.user import User as UserModel

router = APIRouter()


# current_user: UserBase = Depends(get_current_user),
@router.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id,not UserModel.is_deleted).first()
        if not user:
            return UserResponse.create(data=[], success=True,success_message="No hay datos que mostrar")
        return UserResponse.create(data=[user.__dict__], success=True)
    except Exception as e:
        logger.error(f"Error al mostrar el usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al hacer la consulta:{e}")


@router.get("/delete_users/{user_id}", response_model=UserResponse)
async def get_delete_users(db: Session = Depends(get_db)):
    try:
        users = db.query(UserModel).filter(UserModel.is_deleted).all()
        if not users:
            return UserResponse.create(data=[], success=True,success_message="No hay datos que mostrar")
        aux = [a.__dict__ for a in users]
        return UserResponse.create(data=aux, success=True)
    except Exception as e:
        logger.error(f"Error al mostrar el usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al hacer la consulta:{e}")


@router.get("/all_users/{user_id}", response_model=UserResponse, summary='Obtiene todos los usuarios')
async def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(UserModel).where(UserModel.is_deleted== False).all()
        if not users:
            return UserResponse.create(data=[], success=True,success_message="No hay datos que mostrar")
        aux= [a.__dict__ for a in users]
        return UserResponse.create(data=aux, success=True)
    except Exception as e:
        logger.error(f"Error al mostrar el usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al hacer la consulta:{e}")


@router.post("/users/{user_id}", response_model=UserResponse, summary='Crear un nuevo usuario')
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    try:
        obj = UserModel()
        obj.password = hashlib.sha256(user.password.encode()).hexdigest()
        for key, value in user.dict().items():
            setattr(obj, key, value)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return UserResponse.create(data=[obj.__dict__], success=True, success_message='Usuario creado con exito')
    except Exception as e:
        logger.error(f"Error al crear el usuario: {e}")
        return UserResponse.create(data=[], success=False,failure_message=e)


@router.put("/users/{user_id}", response_model=UserResponse, summary='actualizar usuario por su id')
async def update_user(user_id: int, user: UserBase, db: AsyncSession = Depends(get_db)):
    try:
        # Obtener el usuario a actualizar
        result = db.query(UserModel).filter(UserModel.id == user_id).first()
        if result is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Actualizar los campos del usuario
        result.username = user.username
        result.email = user.email
        result.age = user.age
        if user.password:
            result.password = hashlib.sha256(user.password.encode()).hexdigest()
            db.commit()
            db.refresh(result)

        return UserResponse.create(data=[result.__dict__], success=True)
    except Exception as e:
        logger.error(f"Error al crear el usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear el usuario:{e}")


@router.delete("/users/{user_id}", response_model=UserResponse, summary='Eliminar usuario por su id')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        result = db.query(UserModel).filter(UserModel.id == user_id and (not UserModel.is_deleted)).first()

        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        # Marcar el usuario como eliminado
        result.is_deleted = True
        db.commit()
        db.refresh(result)
        return UserResponse.create(data=[result.__dict__], success=True)
    except Exception as e:
        logger.error(f"Error al eliminar el usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario:{e}")
