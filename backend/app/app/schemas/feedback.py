from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field
from app.schemas.feedback_type import FeedbackType


# Shared properties

class FeedbackBase(BaseModel):
    feedback_type: FeedbackType


class FeedbackIn(FeedbackBase):
    pass


# Properties to receive on item creation
class FeedbackCreate(FeedbackBase):
    property_id: int
    user_id: int


# Properties to receive on item update
class FeedbackUpdate(FeedbackBase):
    property_id: int
    user_id: int


# Properties shared by models stored in DB
class FeedbackInDBBase(FeedbackBase):
    id: int
    property_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Feedback(FeedbackInDBBase):
    pass


# Properties properties stored in DB
class FeedbackInDB(FeedbackInDBBase):
    pass



