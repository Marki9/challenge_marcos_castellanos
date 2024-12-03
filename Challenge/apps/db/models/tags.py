from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from apps.db.db import Base
from .post import post_tags
from ...mixins import SoftDeleteMixin, TimestampMixin


class Tag(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True)
    posts = relationship("Post", secondary=post_tags, back_populates="tags")