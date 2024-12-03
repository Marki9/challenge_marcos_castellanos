from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.config import logger
from apps.db.db import get_db
from apps.db.schemas.tags import TagResponse, TagBase
from apps.db.models.tags import Tag as TagModel


router = APIRouter()


@router.get("/Tags/", response_model=TagResponse)
async def get_all_tags( db: AsyncSession = Depends(get_db)):
    try:
        user = db.query(TagModel).all()
        if not user:
            raise HTTPException(status_code=404, detail="No hay datos que mostrar")
        return TagResponse.create(data=[user.__dict__], success=True)
    except Exception as e:
        logger.error(f"Error al mostrar el usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al hacer la consulta:{e}")


@router.get("/Tags/{tag_id}", response_model=TagResponse)
async def get_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    tag = await db.get(TagModel, tag_id)
    if tag is None or tag.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return tag


@router.post("/tags/", response_model=TagResponse)
async def create_tag(tag: TagBase, db: AsyncSession = Depends(get_db)):

    pass


@router.put("/tags/{tag_id}", response_model=TagResponse)
async def update_tag(tag:TagBase,  db: AsyncSession = Depends(get_db)):

    pass


@router.delete("/tag/{tag_id}", response_model=TagResponse)
async def delete_tag(tag: TagBase,  db: AsyncSession = Depends(get_db)):

    pass