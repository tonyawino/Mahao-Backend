from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class PropertyPhoto(Base):
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("property.id"), index=True)
    photo = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    last_updated = Column('last_updated', DateTime, onupdate=func.now())
    property = relationship("Property", back_populates="property_photos")
