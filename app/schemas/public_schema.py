from pydantic import BaseModel
from datetime import datetime

class PublicCapsuleResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_nickname: str
    created_at: datetime

    class Config:
        orm_mode = True
