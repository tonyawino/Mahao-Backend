from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
#from geoalchemy2 import Geometry

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .property_category import PropertyCategory


class Property(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    feature_image = Column(String, nullable=False)
    num_bed = Column(Integer, nullable=False, default=0, index=True)
    num_bath = Column(Integer, nullable=False, default=0, index=True)
    location_name = Column(String, nullable=True, index=True)
    price = Column(Float, nullable=False, default=0, index=True)
    #location = Column(Geometry('POINT'), nullable=False, index=True)
    is_enabled = Column(Boolean, nullable=False, default=True, index=True)
    is_verified = Column(Boolean, nullable=False, default=False, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    property_category_id = Column(Integer, ForeignKey("propertycategory.id"))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    last_updated = Column('last_updated', DateTime, onupdate=func.now())
    owner = relationship("User", back_populates="properties")
    property_category = relationship("PropertyCategory", back_populates="properties")
    property_amenities = relationship("PropertyAmenity", back_populates="property")
    favorites = relationship("Favorite", back_populates="property")
    feedbacks = relationship("Feedback", back_populates="property")
    property_photos = relationship("PropertyPhoto", back_populates="property")

    @hybrid_property
    def is_favorite(self):
        is_fave = (self.favorites is not None and (len(self.favorites) > 0))
        return is_fave
