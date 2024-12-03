from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from apps.config import logger
from apps.db.db import get_db
from apps.db.schemas.post import PostResponse, PostBase
from apps.db.models.post import Post as PostModel


router = APIRouter()


@router.get("/all_posts/{post_id}", response_model=PostResponse)
async def get_all_posts(db: Session = Depends(get_db)):
    try:
        post = db.query(PostModel).filter(not PostModel.is_deleted).all()
        if not post:
            raise HTTPException(status_code=404, detail="No hay datos que mostrar")
        aux = [a.__dict__ for a in post]
        return PostResponse.create(data=aux, success=True)
    except Exception as e:
        logger.error(f"Error al mostrar el post: {e}")
        raise HTTPException(status_code=500, detail=f"Error al hacer la consulta:{e}")


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(PostModel).filter_by(PostModel.id == post_id, not PostModel.is_deleted).first()
        if not post:
            raise HTTPException(status_code=404, detail="No hay datos que mostrar")
        return PostResponse.create(data=[post.__dict__], success=True)
    except Exception as e:
        logger.error(f"Error al mostrar el tag: {e}")
        raise HTTPException(status_code=500, detail=f"Error al hacer la consulta:{e}")


@router.post("/posts/", response_model=PostResponse)
async def create_post(post: PostBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = PostModel()
        for key, value in post.dict().items():
            setattr(obj, key, value)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return PostResponse.create(data=[obj.__dict__], success=True, success_message='Tag creado con exito')
    except Exception as e:
        logger.error(f"Error al crear el usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear el tag:{e}")


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post: PostBase, db: Session= Depends(get_db)):
    try:
        result = db.query(PostModel).filter_by(PostModel.id == post_id, not PostModel.is_deleted)
        if result is None:
            raise HTTPException(status_code=404, detail="no hay datos que mostrar")

        result.titlr = post.title
        result.owner_id = post.owner_id
        result
        db.commit()
        db.refresh(result)

        return PostResponse.create(data=[result.__dict__], success=True)
    except Exception as e:
        logger.error(f"Error al crear el tag: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear el tag:{e}")


@router.delete("/posts/{post_id}", response_model=PostResponse)
async def delete_post(post_id, db: Session=Depends(get_db)):
    try:
        result = db.query(PostModel).filter_by(PostModel.id == post_id,not PostModel.s_deleted)

        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        result.is_deleted = True
        db.commit()
        db.refresh(result)
        return PostResponse(data=[result], success=True)
    except Exception as e:
        logger.error(f"Error al eliminar el usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario:{e}")
