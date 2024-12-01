from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.db.db import get_db
from apps.db.schemas.post import PostResponse, PostBase
from apps.db.models.post import Post as PostModel
from apps.auth.authentication import get_current_user
from apps.db.models.crud_routines.crud import CRUDBase
from apps.db.schemas.user import UserBase

router = APIRouter()



@router.get("/posts/", response_model=PostResponse)
async def get_all_posts(current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    post = await db.get(PostModel, post_id)
    if post is None or post.is_deleted:
        raise HTTPException(status_code=404, detail="post not found")
    return CRUDBase.get_all(db=db)

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, current_user: PostBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    post = await db.get(PostModel, post_id)
    if post is None or post.is_deleted:
        raise HTTPException(status_code=404, detail="post not found")
    return CRUDBase.get(id=user_id, db=db)

@router.post("/posts/", response_model=PostResponse)
async def create_post(post: PostBase, current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    return CRUDBase.create(db=db, obj_in=post)

@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post: PostBase, current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    return CRUDBase.update(db=db, obj_in=post)

@router.delete("/posts/{post_id}", response_model=PostResponse)
async def delete_post(post: PostBase, current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    return CRUDBase.delete(db=db, obj_in=post)