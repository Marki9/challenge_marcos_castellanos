from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from apps.db.db import Base
from .post import post_tags
from apps.mixins import SoftDeleteMixin, TimestampMixin



class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True)
    posts = relationship("Post", secondary=post_tags, back_populates="tags")