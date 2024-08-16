from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Account(BaseModel):
    login: str
    followers: int
    post: int
    email: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_last_post: Optional[datetime] = None
