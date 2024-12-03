from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from apps.config import logger
from apps.db.db import get_db
from apps.db.schemas.tags import TagResponse, TagBase
from apps.db.models.tags import Tag as TagModel


router = APIRouter()


@router.get("/all_Tags/{tag_id}", response_model=TagResponse)
async def get_all_tags( db: Session = Depends(get_db)):
    try:
        tag = db.query(TagModel).filter(not TagModel.is_deleted).all()
        if not tag:
            raise HTTPException(status_code=404, detail="No hay datos que mostrar")
        aux = [a.__dict__ for a in tag]
        return TagResponse.create(data=aux, success=True)
    except Exception as e:
        logger.error(f"Error al mostrar el tag: {e}")
        raise HTTPException(status_code=500, detail=f"Error al hacer la consulta:{e}")


@router.get("/Tags/{tag_id}", response_model=TagResponse)
async def get_tag(tag_id: int, db: Session = Depends(get_db)):
    try:
        tag = db.query(TagModel).filter_by(TagModel.id==tag_id,not TagModel.is_deleted).first()
        if not tag:
            raise HTTPException(status_code=404, detail="No hay datos que mostrar")
        return TagResponse.create(data=[tag.__dict__], success=True)
    except Exception as e:
        logger.error(f"Error al mostrar el tag: {e}")
        raise HTTPException(status_code=500, detail=f"Error al hacer la consulta:{e}")


@router.get("/delete_Tags/{tag_id}", response_model=TagResponse)
async def delete_tags( db: Session = Depends(get_db)):
    try:
        tag = db.query(TagModel).filter_by(TagModel.is_deleted).all()
        if not tag:
            raise HTTPException(status_code=404, detail="No hay datos que mostrar")
        aux = [a.__dict__ for a in tag]
        return TagResponse.create(data=aux, success=True)
    except Exception as e:
        logger.error(f"Error al mostrar el tag: {e}")
        raise HTTPException(status_code=500, detail=f"Error al hacer la consulta:{e}")


@router.post("/tags/", response_model=TagResponse)
async def create_tag(tag: TagBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = TagModel()
        for key, value in tag.dict().items():
            setattr(obj, key, value)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return TagResponse.create(data=[obj.__dict__], success=True, success_message='Tag creado con exito')
    except Exception as e:
        logger.error(f"Error al crear el usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear el tag:{e}")


@router.put("/tags/{tag_id}", response_model=TagResponse)
async def update_tag(tag_id:int, tag:TagBase,  db: Session= Depends(get_db)):
    try:
        result = db.query(TagModel).filter_by(TagModel.id == tag_id, not TagModel.is_deleted)
        if result is None:
            raise HTTPException(status_code=404, detail="no hay datos que mostrar")

        result.text = tag.text
        db.commit()
        db.refresh(result)

        return TagResponse.create(data=[result.__dict__], success=True)
    except Exception as e:
        logger.error(f"Error al crear el tag: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear el tag:{e}")


@router.delete("/tag/{tag_id}", response_model=TagResponse)
async def delete_tag(tag_id:int,  db: Session = Depends(get_db)):
    try:
        result = db.query(TagModel).filter_by(TagModel.id== tag_id, not TagModel.is_deleted)

        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        result.is_deleted = True
        db.commit()
        db.refresh(result)
        return TagResponse.create(data=[result], success=True)
    except Exception as e:
        logger.error(f"Error al eliminar el usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario:{e}")