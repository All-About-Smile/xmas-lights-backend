from datetime import datetime

from pydantic import BaseModel


class LetterCreate(BaseModel):
    writer_nickname: str
    content: str


class LetterResponse(BaseModel):
    id: int
    letter_number: int
    writer_nickname: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
