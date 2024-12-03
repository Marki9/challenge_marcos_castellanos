from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from apps.db.db import get_db
from apps.db.schemas.post import PostResponse, PostBase
from apps.db.models.post import Post as PostModel
# from apps.auth.authentication import get_current_user
from apps.db.schemas.user import UserBase

router = APIRouter()



@router.get("/posts/", response_model=PostResponse)
async def get_all_posts( db: AsyncSession = Depends(get_db)):
    post = await db.get(PostModel)
    if post is None or post.is_deleted:
        raise HTTPException(status_code=404, detail="post not found")
    return post

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(PostModel, post_id)
    if post is None or post.is_deleted:
        raise HTTPException(status_code=404, detail="post not found")
    return post

@router.post("/posts/", response_model=PostResponse)
async def create_post(post: PostBase, db: AsyncSession = Depends(get_db)):

    pass

@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post: PostBase,  db: AsyncSession = Depends(get_db)):

    pass

@router.delete("/posts/{post_id}", response_model=PostResponse)
async def delete_post(post: PostBase, db: AsyncSession = Depends(get_db)):

    pass