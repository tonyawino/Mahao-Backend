from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    profile_picture = Column(String, default=None)
    location = Column(String, nullable=True, default=None)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    items = relationship("Item", back_populates="owner")
