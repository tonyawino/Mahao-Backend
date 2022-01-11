from typing import Optional

from pydantic import BaseModel

from .user import User

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None

class TokenWithUser(BaseModel):
    token_object: Token
    user: User
    access_token: str
    token_type: str