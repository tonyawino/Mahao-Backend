from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl


# Shared properties
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    location: Optional[str] = None
    is_verified: Optional[bool] = False
    is_active: Optional[bool] = True
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    profile_picture: Optional[HttpUrl] = None


class UserInDBBase(UserBase):
    id: int
    profile_picture: Optional[HttpUrl] = None
    created_at: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
