from pydantic import BaseModel
from datetime import datetime

class LetterCreate(BaseModel):
    capsule_id: int
    writer_name: str
    content: str


class LetterResponse(BaseModel):
    id: int
    capsule_id: int
    writer_name: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
