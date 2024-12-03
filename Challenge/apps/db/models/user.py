import hashlib
import logging
from fastapi import HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.asyncio import AsyncSession

# from apps.auth.auth_handler import verify_password
from apps.db.db import Base
from apps.mixins import SoftDeleteMixin, TimestampMixin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

logger = logging.getLogger("uvicorn.error")


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    age = Column(Integer, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    posts = relationship("Post", back_populates="owner")


    @classmethod
    async def get_value(cls, db_session: Session, name: str):
        """Recupera una instancia de usuario de la base de datos por nombre de usuario."""
        try:
            # Consulta la tabla User para encontrar un usuario con el nombre de usuario dado
            # result = await db_session.execute(select(cls).filter_by(username=name))
            # user = result.scalar_one()
            aux = db_session.query(User).filter(User.username == name, not User.is_deleted).first()
            # user_instance = await user.get_instance(db_session, name)
            return aux
        except NoResultFound:
            # Devuelve None o lanza una excepción si no se encuentra el usuario
            return None

    def get_user(self, db: AsyncSession, username: str):
        if username in db:
            user_dict = db[username]
            return User(**user_dict)


