# app/services/auth_service.py

from datetime import timedelta
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user_schema import UserResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings


def register_user(data: RegisterRequest) -> UserResponse:
    """
    회원가입 로직
    - 이메일 중복 체크
    - 비밀번호 해싱
    - User 모델 생성 & DB 저장
    - UserResponse 반환
    """
    # TODO: DB 붙일 때 구현
    # - hashed_pw = hash_password(data.password)
    # - user = User(...)
    # - db에 저장
    raise NotImplementedError


def authenticate_user(data: LoginRequest) -> UserResponse | None:
    """
    로그인 시도 로직
    - 이메일로 유저 찾기
    - 비밀번호 검증
    - 성공 시 User 정보 반환, 실패 시 None
    """
    # TODO: DB에서 유저 찾고 verify_password 사용
    raise NotImplementedError


def create_login_token(user: UserResponse) -> TokenResponse:
    """
    로그인 성공 후 JWT 액세스 토큰 생성
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token = create_access_token(
        data={"sub": user.email},  # 토큰 subject에 email 사용
        expires_delta=access_token_expires,
    )

    return TokenResponse(access_token=token)
