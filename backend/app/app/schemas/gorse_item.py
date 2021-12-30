from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class GorseItem(BaseModel):
    Categories: List[str]
    Comment: str
    IsHidden: bool
    ItemId: str
    Labels: List[str]
    Timestamp: datetime



