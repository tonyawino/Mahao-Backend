from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .property_category import PropertyCategory


class Favorite(Base):
    property_id = Column(Integer, ForeignKey("property.id"), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    last_updated = Column('last_updated', DateTime, onupdate=func.now())
    property = relationship("Property", back_populates="favorites")
    user = relationship("User", back_populates="favorites")
