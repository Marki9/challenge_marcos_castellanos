from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from apps.db.db import Base
from apps.mixins import SoftDeleteMixin, TimestampMixin
from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    age = Column(Integer, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    posts = relationship("Post", back_populates="owner")

