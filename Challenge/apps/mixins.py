from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.sql import func

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False)

class TimestampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())