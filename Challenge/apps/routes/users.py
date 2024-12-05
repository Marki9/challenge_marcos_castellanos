import hashlib
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from apps.auth.auth_handler import get_password_hash
from apps.auth.authentication import get_current_user
from apps.config import logger
from apps.db.db import get_db
from apps.db.schemas.user import UserResponse, UserBase
from apps.db.models.user import User as UserModel

router = APIRouter()


# current_user: UserBase = Depends(get_current_user),
@router.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db),
                   current_user: UserModel = Security(get_current_user, scopes=["me"])):
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id,not UserModel.is_deleted).first()
        if not user:
            return UserResponse.create(data=[], success=True,success_message="No hay datos que mostrar")
        return UserResponse.create(data=[user.__dict__], success=True)
    except Exception as e:
        logger.error(f"Error al mostrar el usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al hacer la consulta:{e}")


@router.get("/delete_users/{user_id}", response_model=UserResponse)
async def get_delete_users(db: Session = Depends(get_db),
                           current_user: UserModel = Security(get_current_user, scopes=["me"])):
    try:
        users=[]
        users = db.query(UserModel).filter(UserModel.is_deleted== True).all()
        if not users:
            return UserResponse(data=[], success=True,cont=0, success_message="No hay datos que mostrar")
        return UserResponse(data=users,count=len(users), success=True, message='Operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.get("/all_users/{user_id}", response_model=UserResponse, summary='Obtiene todos los usuarios')
async def get_all_users(db: Session = Depends(get_db),
                        current_user: UserModel = Security(get_current_user, scopes=["me"])):
    try:
        users = db.query(UserModel).where(UserModel.is_deleted == False).all()
        if not users:
            return UserResponse(data=[], success=True, cont=0,success_message="No hay datos que mostrar")
        return UserResponse(data=users, count=len(users), success=True, message='Operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.post("/users/{user_id}", response_model=UserResponse, summary='Crear un nuevo usuario')
async def create_user(user: UserBase, db: Session = Depends(get_db),
                      # current_user: UserModel = Security(get_current_user, scopes=["me"])
                      ):
    try:
        obj = UserModel()
        for key, value in user.dict().items():
            setattr(obj, key, value)
        obj.password = get_password_hash(user.password)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return UserResponse(data=[obj],count=1, success=True, message='Operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.put("/users/{user_id}", response_model=UserResponse, summary='actualizar usuario por su id')
async def update_user(user_id: int, user: UserBase, db: AsyncSession = Depends(get_db),
                      current_user: UserModel = Security(get_current_user, scopes=["me"])):
    try:
        result=[]
        result = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_deleted == False).first()
        if result is None:
            return UserResponse(data=[], success=True, cont=0, success_message="No se encontró registro q coincida con este id")
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        result.username = user.username
        result.email = user.email
        result.age = user.age
        if user.password:
            result.password = get_password_hash(password=user.password)
            db.commit()
            db.refresh(result)

        return UserResponse(data=[result],count=1, success=True , message='Operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.delete("/users/{user_id}", response_model=UserResponse, summary='Eliminar usuario por su id')
async def delete_user(user_id: int, db: Session = Depends(get_db),
                      current_user: UserModel = Security(get_current_user, scopes=["me"])):
    try:
        result = db.query(UserModel).filter(UserModel.id == user_id and (not UserModel.is_deleted)).first()
        if result:
            # Marcar el usuario como eliminado
            db.commit()
            db.refresh(result)
        return UserResponse.create(data=[result], success=True,count=1,message='operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")
