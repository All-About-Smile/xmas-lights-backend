from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.redis import redis_client
from app.core.security import (create_access_token, generate_refresh_token,
                               hash_password, verify_password)
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.auth_schema import (LoginRequest, RefreshRequest,
                                     RegisterRequest, TokenResponse)
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    # userid 중복 체크
    if db.query(User).filter(User.userid == payload.userid).first():
        raise HTTPException(status_code=400, detail="UserID already taken")

    # email 중복 체크
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        userid=payload.userid,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user



@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userid == payload.userid).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect userid or password")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect userid or password")

    # Access Token 생성
    access_token = create_access_token({"sub": str(user.id)})

    # Refresh Token 생성 & Redis 저장
    refresh_token = generate_refresh_token()
    redis_client.set(
        f"refresh:{refresh_token}",
        str(user.id),
        ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    key = f"refresh:{payload.refresh_token}"
    user_id = redis_client.get(key)

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Rotation: 기존 refresh 제거
    redis_client.delete(key)

    new_refresh = generate_refresh_token()
    redis_client.set(
        f"refresh:{new_refresh}",
        str(user.id),
        ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )

    new_access = create_access_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
    )


@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
