from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base
from app.mixins import SoftDeleteMixin, TimestampMixin

class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    age= Column(int, index= True)
    email= Column(str, unique=True,index=True)
    posts = relationship("Post", back_populates="owner")
    
    
    @classmethod
    def get_instance(cls, db_session: Session, name: str):
        """Recupera una instancia de usuario de la base de datos por nombre de usuario."""
        try:
            # Consulta la tabla User para encontrar un usuario con el nombre de usuario dado
            user = db_session.query(cls).filter_by(username=name).one()
            return user
        except NoResultFound:
            # Devuelve None o lanza una excepción si no se encuentra el usuario
            return None
