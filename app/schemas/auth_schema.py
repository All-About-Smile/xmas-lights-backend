from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    userid: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    userid: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: str