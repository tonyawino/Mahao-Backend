from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from . import User, PropertyCategory
from .geometry import Geometry


# Shared properties
class PropertyBase(BaseModel):
    property_category_id: int
    title: str
    description: str
    num_bed: int = Field(..., ge=0, title="Number of bedrooms")
    num_bath: int = Field(..., ge=0, title="Number of bathrooms")
    location_name: Optional[str] = None
    price: float = Field(..., ge=100, title="Rent per month")
    #location: Geometry
    is_enabled: Optional[bool] = True
    is_verified: Optional[bool] = False


# Properties to receive on item creation
class PropertyCreate(PropertyBase):
    feature_image: Optional[str]


# Properties to receive on item update
class PropertyUpdate(PropertyBase):
    feature_image: Optional[str]


# Properties shared by models stored in DB
class PropertyInDBBase(PropertyBase):
    id: int
    owner_id: int
    feature_image: str
    created_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Property(PropertyInDBBase):
    owner: User
    property_category: PropertyCategory


# Properties properties stored in DB
class PropertyInDB(PropertyInDBBase):
    pass


