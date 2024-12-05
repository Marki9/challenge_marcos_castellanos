from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from apps.auth.authentication import get_current_user
from apps.config import logger
from apps.db.db import get_db
from apps.db.models.user import User
from apps.db.schemas.post import PostResponse, PostBase
from apps.db.models.post import post_tags, Post as PostModel
from apps.db.models.tags import Tag

router = APIRouter()


@router.get("/all_posts/{post_id}", response_model=PostResponse)
async def get_all_posts(db: Session = Depends(get_db),
                        current_user: User = Security(get_current_user, scopes=["me"])):
    try:
        post=[]
        post = db.query(PostModel).filter(PostModel.is_deleted == False).all()
        if not post:
            raise HTTPException(status_code=404, detail="No hay datos que mostrar")
        return PostResponse(data=post, success=True, count=len(post),  message='Operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db),
                   current_user: User = Security(get_current_user, scopes=["me"])):
    try:
        post = db.query(PostModel).filter(PostModel.id == post_id, PostModel.is_deleted == False).first()
        if not post:
            return PostResponse(data=[], success=True, count=0, message='No hay datos que mostrar')
        return PostResponse(data=[post], count=1, success=True, message='Operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.post("/posts/{post_id}", response_model=PostResponse)
async def create_post(post: PostBase, db: AsyncSession = Depends(get_db),
                      current_user: User = Security(get_current_user, scopes=["me"])):
    try:
        obj = PostModel(title=post.title, content=post.content )
        obj.owner_id = current_user.id
        if post.tags:
            for row in post.tags:
                new_tag = Tag(text=row.text)
                db.add(new_tag)
                obj.tags.append(new_tag)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return PostResponse(data=[obj], count=1, success=True, message='Operación exitosa')
    except Exception as e:
        logger.error(f"Error {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post: PostBase, db: Session = Depends(get_db),
                      current_user: User = Security(get_current_user, scopes=["me"])):
    try:
        result = db.query(PostModel).filter(PostModel.id == post_id, PostModel.is_deleted == False).first()
        if result is None:
            return PostResponse(data=[], success=False, count=0, message='No se encontró ningun registro con ese id')
        if current_user.id != result.owner_id:
            raise HTTPException(status_code=403, detail="ESte usuario no fue el que creó este post")

        result.title = post.title
        result.owner_id = current_user.id
        if post.tags:
            for row in post.tags:
                new_tag = Tag(text=row.text)
                db.add(new_tag)  #
                result.tags.append(new_tag)
        db.commit()
        db.refresh(result)

        return PostResponse(data=[result], count=1, success=True, message='Operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.delete("/posts/{post_id}", response_model=PostResponse)
async def delete_post(post_id, db: Session = Depends(get_db),
                      current_user: User = Security(get_current_user, scopes=["me"])):
    try:
        result = db.query(PostModel).filter(PostModel.id == post_id, PostModel.is_deleted == False).first()

        if result is None:
            return PostResponse(data=[], success=False, count=0, message='No se encontró ningun registro con ese id')
        if current_user.id != result.owner_id:
            raise HTTPException(status_code=403, detail="ESte usuario no fue el que creó este post")

        result.is_deleted = True
        db.commit()
        db.refresh(result)
        return PostResponse(data=[result], success=True, count=1, message='Operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")
