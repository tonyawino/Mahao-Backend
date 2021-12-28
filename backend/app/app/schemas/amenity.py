from datetime import datetime
from typing import Optional

from fastapi import File
from pydantic import BaseModel, HttpUrl


# Shared properties
class AmenityBase(BaseModel):
    title: str
    description: str


# Properties to receive on item creation
class AmenityCreate(AmenityBase):
    icon: Optional[str]


# Properties to receive on item update
class AmenityUpdate(AmenityBase):
    icon: Optional[str]


# Properties shared by models stored in DB
class AmenityInDBBase(AmenityBase):
    id: int
    icon: Optional[HttpUrl]
    created_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Amenity(AmenityInDBBase):
    pass


# Properties properties stored in DB
class AmenityInDB(AmenityInDBBase):
    pass
