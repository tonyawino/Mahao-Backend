from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class GorseFeedback(BaseModel):
    Comment: str
    FeedbackType: str
    ItemId: str
    UserId: str
    Timestamp: datetime



