from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field, StringConstraints, validator

from app.constants.ornament import (
    PublicOrnamentColor,
    PublicOrnamentShape,
)

Password4Digit = Annotated[str, StringConstraints(pattern=r"^\d{4}$")]


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
    total_count: int
    total_pages: int


class LetterCreateRequest(BaseModel):
    writer_nickname: str
    content: str = Field(..., max_length=200)
    ornament_shape: PublicOrnamentShape
    ornament_color: PublicOrnamentColor
    password_for_edit: Password4Digit | None = None

    @validator("writer_nickname", "content", pre=True)
    def _strip_text_fields(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value

    @validator("writer_nickname")
    def _validate_writer_nickname(cls, value):
        if not value:
            raise ValueError("writer_nickname must not be empty")
        if len(value) > 7:
            raise ValueError("writer_nickname must be at most 7 characters")
        return value

    @validator("content")
    def _validate_content(cls, value):
        if not value:
            raise ValueError("content must not be empty")
        return value

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
    writer_nickname: Optional[str] = None
    content: Optional[str] = Field(default=None, max_length=200)
    ornament_shape: Optional[PublicOrnamentShape] = None
    ornament_color: Optional[PublicOrnamentColor] = None
    password: Password4Digit = Field(..., description="편지 수정용 비밀번호")

    @validator("writer_nickname", "content", pre=True)
    def _strip_optional_text_fields(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value

    @validator("writer_nickname")
    def _validate_optional_writer_nickname(cls, value):
        if value is None:
            return value
        if not value:
            raise ValueError("writer_nickname must not be empty")
        if len(value) > 7:
            raise ValueError("writer_nickname must be at most 7 characters")
        return value

    @validator("content")
    def _validate_optional_content(cls, value):
        if value is None:
            return value
        if not value:
            raise ValueError("content must not be empty")
        return value


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
