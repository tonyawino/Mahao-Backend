from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# Shared properties

class PropertyPhotoBase(BaseModel):
    photo: str


class PropertyPhotoIn(PropertyPhotoBase):
    pass


# Properties to receive on item creation
class PropertyPhotoCreate(PropertyPhotoBase):
    property_id: int


# Properties to receive on item update
class PropertyPhotoUpdate(PropertyPhotoBase):
    property_id: int


# Properties shared by models stored in DB
class PropertyPhotoInDBBase(PropertyPhotoBase):
    id: int
    property_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class PropertyPhoto(PropertyPhotoInDBBase):
    pass


# Properties properties stored in DB
class PropertyPhotoInDB(PropertyPhotoInDBBase):
    pass


class PropertyPhotoRemove(BaseModel):
    id: int
