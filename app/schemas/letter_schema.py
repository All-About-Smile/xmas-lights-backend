from datetime import datetime

from pydantic import BaseModel


class LetterCreate(BaseModel):
    writer_nickname: str
    content: str

class LetterListItem(BaseModel):
    letter_number: int
    writer_nickname: str
    ornament_shape: str
    ornament_color: str
    is_event_ornament: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class LetterListResponse(BaseModel):
    items: list[LetterListItem]
    limit: int
    offset: int
    has_next: bool

class LetterCreateRequest(BaseModel):
    writer_nickname: str
    content: str
    ornament_shape: str
    ornament_color: str
    created_at: datetime
    password_for_edit: str

    class Config:
        from_attributes = True

class LetterDetailResponse(BaseModel):
    letter_number: int
    writer_nickname: str
    content: str
    ornament_shape: str
    ornament_color: str
    is_event_ornament: bool
    created_at: datetime

    class Config:
        from_attributes = True