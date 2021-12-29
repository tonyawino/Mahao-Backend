from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .property_category import PropertyCategory


class PropertyAmenity(Base):
    property_id = Column(Integer, ForeignKey("property.id"), primary_key=True, index=True)
    amenity_id = Column(Integer, ForeignKey("amenity.id"), primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    property = relationship("Property", back_populates="property_amenities")
    amenity = relationship("Amenity", back_populates="property_amenities")
