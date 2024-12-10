from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_mixin,declared_attr
@declarative_mixin
class SoftDeleteMixin:
    @declared_attr
    def is_deleted(cls):
        return Column('is_deleted',Boolean, default=False)
    
    def delete(self, session):
        self.is_deleted = True
        session.add(self)
        session.commit()

@declarative_mixin
class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column('created_at',DateTime,nullable=False, default=func.now())
   
    @declared_attr
    def updated_at(cls):
        return Column('updated_at',DateTime,nullable=False, default=func.now(), onupdate=func.now())