from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LetterCreate(BaseModel):
    writer_nickname: str
    content: str


class LetterList(BaseModel):
    letter_number: int
    writer_nickname: str
    ornament_shape: str
    ornament_color: str
    is_event_ornament: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
