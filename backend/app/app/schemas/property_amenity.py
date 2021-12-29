from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

# Shared properties
from app.schemas import Amenity


class PropertyAmenityBase(BaseModel):
    property_id: int
    amenity_id: int


# Properties to receive on item creation
class PropertyAmenityCreate(PropertyAmenityBase):
    pass


# Properties to receive on item update
class PropertyAmenityUpdate(PropertyAmenityBase):
    pass


# Properties shared by models stored in DB
class PropertyAmenityInDBBase(PropertyAmenityBase):
    created_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class PropertyAmenity(PropertyAmenityInDBBase):
    amenity: Amenity


# Properties properties stored in DB
class PropertyAmenityInDB(PropertyAmenityInDBBase):
    pass


class PropertyAmenityModify(BaseModel):
    added: Optional[List[int]] = None
    removed: Optional[List[int]] = None
