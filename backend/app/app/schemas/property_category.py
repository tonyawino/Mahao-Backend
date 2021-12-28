from datetime import datetime
from typing import Optional

from fastapi import File
from pydantic import BaseModel, HttpUrl


# Shared properties
class PropertyCategoryBase(BaseModel):
    title: str
    description: str


# Properties to receive on item creation
class PropertyCategoryCreate(PropertyCategoryBase):
    icon: Optional[str]


# Properties to receive on item update
class PropertyCategoryUpdate(PropertyCategoryBase):
    icon: Optional[str]


# Properties shared by models stored in DB
class PropertyCategoryInDBBase(PropertyCategoryBase):
    id: int
    icon: Optional[HttpUrl]
    created_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class PropertyCategory(PropertyCategoryInDBBase):
    pass


# Properties properties stored in DB
class PropertyCategoryInDB(PropertyCategoryInDBBase):
    pass
