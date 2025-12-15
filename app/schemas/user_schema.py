from datetime import datetime

from pydantic import BaseModel, EmailStr

# 공통 필드(email/nickname)
class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True

# 요청 DTO
class UserCreate(BaseModel):
    userid: str
    email: EmailStr
    password: str
    
# 응답 DTO
class UserResponse(BaseModel):
    id: int
    userid: str
    email: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }