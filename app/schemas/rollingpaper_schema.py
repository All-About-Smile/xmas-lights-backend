from datetime import datetime
from pydantic import BaseModel


class RollingPaperCreate(BaseModel):
    title: str
    content: str
    open_at: datetime  # 언제 열리는지
    is_public: bool = False


class RollingPaperUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    open_at: datetime | None = None
    is_public: bool | None = None


class RollingPaperResponse(BaseModel):
    id: int
    title: str
    content: str
    open_at: datetime
    is_public: bool
    created_at: datetime

    class Config:
        orm_mode = True
