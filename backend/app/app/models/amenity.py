from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Amenity(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)
    description = Column(String)
    icon = Column(String)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    last_updated = Column('last_updated', DateTime, onupdate=func.now())
    property_amenities = relationship("PropertyAmenity", back_populates="amenity")
