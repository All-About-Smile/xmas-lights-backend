from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.api.letters import get_letters_by_user_id
from app.core.deps import get_current_user
from app.core.exceptions import AppException, ErrorCodes
from app.core.responses import CommonResponse
from app.db.models.letter import Letter
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.letter_schema import LetterResponse
from app.schemas.user_schema import UserResponse, UserUpdateRequest

router = APIRouter(prefix="/users", tags=["users"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/me", response_model=CommonResponse[UserResponse])
def read_me(current_user: CurrentUser):
    return CommonResponse(
        data=UserResponse.model_validate(current_user)
    )


@router.patch("/me", response_model=CommonResponse[UserResponse])
def update_me(
    payload: UserUpdateRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    if payload.email is not None:
        # 이메일 중복 체크
        exists = (
            db.query(User)
            .filter(User.email == payload.email, User.id != current_user.id)
            .first()
        )
        if exists:
            raise AppException(
                code=ErrorCodes.USER_ALREADY_EXISTS,
                message="Email already registered",
            )
        current_user.email = payload.email

    db.commit()
    db.refresh(current_user)

    return CommonResponse(
        data=UserResponse.model_validate(current_user)
    )

@router.get("/{userid}/letters", response_model=CommonResponse[dict])
def read_user_letters(
    userid: str,
    db: DBSession,
    limit: int = Query(8, ge=1, le=20),
    offset: int = Query(0, ge=0),
):
    # 1️) 유저 존재 확인
    user = db.query(User).filter(User.userid == userid).first()
    if not user:
        raise AppException(
            code=ErrorCodes.USER_NOT_FOUND,
            message="User not found",
        )

    # 2️) 편지 조회 (페이징)
    letters = (
        db.query(Letter)
        .filter(
            Letter.user_id == user.id,
            Letter.is_deleted == False,
        )
        .order_by(Letter.created_at)
        .limit(limit + 1)   # has_next 판단용
        .offset(offset)
        .all()
    )

    # 3️) has_next 계산
    has_next = len(letters) > limit
    letters = letters[:limit]

    # 4️) 응답 변환
    data = {
        "items": [LetterResponse.model_validate(l) for l in letters],
        "limit": limit,
        "offset": offset,
        "has_next": has_next,
    }

    return CommonResponse(data=data)
