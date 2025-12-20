from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.exceptions import AppException, AuthException, ErrorCodes
from app.core.redis import redis_client
from app.core.responses import CommonResponse
from app.core.security import (create_access_token, generate_refresh_token,
                               hash_password, verify_password)
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.auth_schema import (LoginRequest, PasswordChangeRequest,
                                     RegisterRequest, TokenResponse)
from app.schemas.user_schema import UserResponse
from app.services.auth_service import register_user

router = APIRouter(prefix="/auth", tags=["auth"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


# =====================
# Register
# =====================
@router.post("/register", response_model=CommonResponse[UserResponse])
def register(payload: RegisterRequest, db: DBSession):
    user = register_user(db=db, payload=payload)

    return CommonResponse(
        data=UserResponse.model_validate(user)
    )


# =====================
# Login
# =====================
@router.post("/login", response_model=CommonResponse[TokenResponse])
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

    refresh_token = generate_refresh_token()
    redis_client.set(
        f"refresh:{refresh_token}",
        str(user.id),
        ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/auth",
    )

    return CommonResponse(
        data=TokenResponse(access_token=access_token)
    )


# =====================
# Refresh
# =====================
@router.post("/refresh", response_model=CommonResponse[TokenResponse])
def refresh_token(
    response: Response,
    db: DBSession,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    if refresh_token is None:
        raise AuthException(
            code=ErrorCodes.AUTH_INVALID_TOKEN,
            message="Missing refresh token",
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
        raise AppException(
            code=ErrorCodes.USER_NOT_FOUND,
            message="User not found",
        )

    # rotation
    redis_client.delete(key)
    new_refresh = generate_refresh_token()
    redis_client.set(
        f"refresh:{new_refresh}",
        str(user.id),
        ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )

    new_access = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/auth",
    )

    return CommonResponse(
        data=TokenResponse(access_token=new_access)
    )


# =====================
# Logout
# =====================
@router.post("/logout", response_model=CommonResponse[dict])
def logout(
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    if refresh_token:
        redis_client.delete(f"refresh:{refresh_token}")

    response.delete_cookie(key="refresh_token", path="/auth")

    return CommonResponse(
        data={"detail": "Logged out successfully"}
    )


# =====================
# password
# =====================
@router.post(
    "/password",
    response_model=CommonResponse[dict],
)
def change_password(
    payload: PasswordChangeRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    if not verify_password(payload.current_password, current_user.password_hash):
        raise AuthException(
            code=ErrorCodes.AUTH_INVALID_CREDENTIALS,
            message="Current password is incorrect",
        )

    current_user.password_hash = hash_password(payload.new_password)
    db.commit()

    return CommonResponse(data={"detail": "Password updated successfully"})
