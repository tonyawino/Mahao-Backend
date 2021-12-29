from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

# Shared properties
from app.schemas import Property


class FavoriteBase(BaseModel):
    property_id: int
    user_id: int


# Properties to receive on item creation
class FavoriteCreate(FavoriteBase):
    pass


# Properties to receive on item update
class FavoriteUpdate(FavoriteBase):
    pass


# Properties shared by models stored in DB
class FavoriteInDBBase(FavoriteBase):
    created_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Favorite(FavoriteInDBBase):
    property: Property


# Properties properties stored in DB
class FavoriteInDB(FavoriteInDBBase):
    pass
