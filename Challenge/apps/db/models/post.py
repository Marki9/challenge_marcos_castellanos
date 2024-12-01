from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base
from app.mixins import SoftDeleteMixin, TimestampMixin

class Post(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nulleable= False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    owner = relationship("User", back_populates="posts")
