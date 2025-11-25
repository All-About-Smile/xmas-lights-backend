from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    id: int
    email: EmailStr
    nickname: str | None = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: str | None = None


class UserResponse(UserBase):
    created_at: datetime