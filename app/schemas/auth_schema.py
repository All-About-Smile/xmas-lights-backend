from pydantic import BaseModel, EmailStr

# 회원가입 요청
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str | None = None


# 로그인 요청
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# 토큰 응답
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"