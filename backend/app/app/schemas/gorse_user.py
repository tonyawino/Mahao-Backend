from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class GorseUser(BaseModel):
    Subscribe: List[str]
    Comment: str
    UserId: str
    Labels: List[str]



