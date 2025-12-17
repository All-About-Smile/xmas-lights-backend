from datetime import datetime

from pydantic import BaseModel, Field

from typing import Optional


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
        
class LetterUpdateRequest(BaseModel):
    content: Optional[str] = None
    ornament_shape: Optional[str] = None
    ornament_color: Optional[str] = None
    password: str = Field(..., description="편지 수정용 비밀번호")
    
class LetterEditResponse(BaseModel):
    letter_number: int
    writer_nickname: str
    content: str
    ornament_shape: str
    ornament_color: str

    class Config:
        from_attributes = True
    
class LetterPasswordRequest(BaseModel):
    password: str = Field(..., description="편지 삭제용 비밀번호")
    