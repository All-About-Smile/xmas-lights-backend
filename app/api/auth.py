from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.exceptions import AppException, AuthException, ErrorCodes
from app.core.redis import redis_client
from app.core.responses import CommonResponse
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    verify_password,
)
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])
DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/register", response_model=UserResponse)
def register(payload: RegisterRequest, db: DBSession):
    if db.query(User).filter(User.userid == payload.userid).first():
        raise AppException(
            code=ErrorCodes.USER_ALREADY_EXISTS, message="UserID already taken"
        )

    if db.query(User).filter(User.email == payload.email).first():
        raise AppException(
            code=ErrorCodes.USER_ALREADY_EXISTS, message="Email already registered"
        )

    user = User(
        userid=payload.userid,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return CommonResponse(data=user)


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    response: Response,
    db: DBSession,
):
    user = db.query(User).filter(User.userid == payload.userid).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise AuthException(
            code=ErrorCodes.AUTH_INVALID_CREDENTIALS,
            message="Incorrect userid or password",
        )

    access_token = create_access_token({"sub": str(user.id)})

    # Refresh Token 생성 & 저장
    refresh_token = generate_refresh_token()
    redis_client.set(
        f"refresh:{refresh_token}",
        str(user.id),
        ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )

    # HttpOnly Cookie 설정
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,  # prod에서는 True
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/auth",
    )

    return CommonResponse(data=TokenResponse(access_token=access_token))


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    response: Response,
    db: DBSession,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    if refresh_token is None:
        raise AuthException(
            code=ErrorCodes.AUTH_INVALID_TOKEN, message="Missing refresh token"
        )

    key = f"refresh:{refresh_token}"
    user_id = redis_client.get(key)

    if user_id is None:
        raise AuthException(
            code=ErrorCodes.AUTH_INVALID_TOKEN,
            message="Invalid or expired refresh token",
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise AppException(code=ErrorCodes.USER_NOT_FOUND, message="User not found")

    # 🔁 Rotation
    redis_client.delete(key)
    new_refresh = generate_refresh_token()
    redis_client.set(
        f"refresh:{new_refresh}",
        str(user.id),
        ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )

    # 새 access token
    new_access = create_access_token({"sub": str(user.id)})

    # 새 refresh cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/auth",
    )

    return CommonResponse(data=TokenResponse(access_token=new_access))


@router.post("/logout")
def logout(
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    if refresh_token:
        redis_client.delete(f"refresh:{refresh_token}")

    # Cookie 제거
    response.delete_cookie(key="refresh_token", path="/auth")

    return CommonResponse(data={"detail": "Logged out successfully"})


@router.get("/me", response_model=UserResponse)
def read_me(current_user: CurrentUser):
    return CommonResponse(data=current_user)
