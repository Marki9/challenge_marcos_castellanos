from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.db.db import get_db
from apps.db.schemas.tags import TagResponse, TagBase
from apps.db.models.tags import Tag as TagModel
from apps.auth.authentication import get_current_user
from apps.db.models.crud_routines.crud import CRUDBase

router = APIRouter()



@router.get("/Tags/", response_model=TagResponse)
async def get_all_tags(current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    tag = await db.get(TagModel, tag_id)
    if tag is None or tag.is_deleted:
        raise HTTPException(status_code=404, detail="Tag not found")
    return CRUDBase.get_all(db=db)

@router.get("/Tags/{tag_id}", response_model=TagResponse)
async def get_tag(tag_id: int, current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    tag_id = await db.get(TagModel, tag_id)
    if tag is None or tag.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return CRUDBase.get(id=tag_id, db=db)

@router.post("/tags/", response_model=TagResponse)
async def create_tag(tag: TagBase, current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    return CRUDBase.create(db=db, obj_in=tag)

@router.put("/tags/{tag_id}", response_model=TagResponse)
async def update_tag(tag:TagBase, current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    return CRUDBase.update(db=db, obj_in=tag)

@router.delete("/tag/{tag_id}", response_model=TagResponse)
async def delete_tag(tag: TagBase, current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    return CRUDBase.delete(db=db, obj_in=tag)