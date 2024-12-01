from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.db.db import get_db
from apps.db.schemas.user import UserResponse, UserBase
from apps.db.models.user import User as UserModel
from apps.auth.authentication import get_current_user
from apps.db.models.crud_routines.crud import CRUDBase

router = APIRouter()



@router.get("/users/", response_model=UserResponse)
async def get_all_users(current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await db.get(UserModel, user_id)
    if user is None or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return CRUDBase.get_all(db=db)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await db.get(UserModel, user_id)
    if user is None or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return CRUDBase.get(id=user_id, db=db)

@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserBase, current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    return CRUDBase.create(db=db, obj_in=user)

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user: UserBase, current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    return CRUDBase.update(db=db, obj_in=user)

@router.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user(user: UserBase, current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    return CRUDBase.delete(db=db, obj_in=user)
