from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from apps.auth.authentication import get_current_user
from apps.config import logger
from apps.db.db import get_db
from apps.db.models.post import Post
from apps.db.models.user import User
from apps.db.schemas.tags import TagResponse, TagBase
from apps.db.models.tags import Tag as TagModel

router = APIRouter()


@router.get("/all_Tags/{tag_id}", response_model=TagResponse)
async def get_all_tags(db: Session = Depends(get_db),
                       current_user: User = Security(get_current_user, scopes=["me"])):
    try:
        tag = []
        tag = db.query(TagModel).filter(TagModel.is_deleted == False).all()
        if not tag:
            return TagResponse(data=tag, success=True, count=len(tag), message='No hay datos que mostrar')
        return TagResponse(data=tag, success=True, count=len(tag), message='operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.get("/Tags/{tag_id}", response_model=TagResponse)
async def get_tag(tag_id: int, db: Session = Depends(get_db),
                  current_user: User = Security(get_current_user, scopes=["me"])):
    try:
        tag = db.query(TagModel).filter_by(TagModel.id == tag_id, TagModel.is_deleted == False).first()
        if not tag:
            return TagResponse(data=tag, success=True, count=len(tag), message='No hay datos que mostrar')
        return TagResponse(data=tag, success=True, count=len(tag), message='operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.get("/delete_Tags/{tag_id}", response_model=TagResponse)
async def delete_tags(db: Session = Depends(get_db),
                      current_user: User = Security(get_current_user, scopes=["me"])):
    try:
        tag = db.query(TagModel).filter(TagModel.is_deleted == False).all()
        if not tag:
            return TagResponse(data=tag, success=True, count=len(tag), message='No hay datos que mostrar')
        return TagResponse(data=tag, success=True, count=len(tag), message='operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.post("/tags/", response_model=TagResponse)
async def create_tag(tag: TagBase, db: AsyncSession = Depends(get_db),
                     current_user: User = Security(get_current_user, scopes=["me"])):
    try:
        obj = TagModel()
        for key, value in tag.dict().items():
            setattr(obj, key, value)
        if tag.posts:
            for row in tag.posts:
                new_post = Post(title=row.title,
                                content=row.content,
                                owner_id=row.owner_id)
                db.add(new_post)
                obj.tags.append(new_post)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return TagResponse(data=[obj], success=True, count=1, message='operación exitosa')
    except Exception as e:
        logger.error(f"Error al : {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.put("/tags/{tag_id}", response_model=TagResponse)
async def update_tag(tag_id: int, tag: TagBase, db: Session = Depends(get_db),
                     current_user: User = Security(get_current_user, scopes=["me"])):
    try:
        result = []
        result = db.query(TagModel).filter_by(TagModel.id == tag_id, TagModel.is_deleted == False)
        if result is None:
            return TagResponse(data=result, success=False, count=0, message='No se encontró el registro con ese id')
        if current_user.id != result.owner_id:
            raise HTTPException(status_code=401, detail="ESte usuario no fue el que creó este post")

        result.text = tag.text
        db.commit()
        db.refresh(result)

        return TagResponse(data=result, success=True, count=1, message='operación exitosa')
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")


@router.delete("/tag/{tag_id}", response_model=TagResponse)
async def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    try:
        result = []
        result = db.query(TagModel).filter_by(TagModel.id == tag_id, TagModel.is_deleted == False)

        if result is None:
            return TagResponse(data=result, success=False, count=0, message='No se encontró el registro con ese id')

        result.is_deleted = True
        db.commit()
        db.refresh(result)
        return TagResponse(data=result, success=True, count=1, message='operación exitosa')
    except Exception as e:
        logger.error(f"Error : {e}")
        raise HTTPException(status_code=500, detail=f"Error:{e}")
