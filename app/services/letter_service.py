# app/services/letter_service.py

from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.exceptions import AppException, ErrorCodes
from app.core.security import hash_password
from app.db.models.letter import Letter
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.letter_schema import LetterCreateRequest, LetterListItem

router = APIRouter(prefix="/users", tags=["users"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.exceptions import AppException, ErrorCodes
from app.db.models.letter import Letter
from app.db.models.user import User
from app.db.session import get_db


def create_letter(
    db: Session,
    *,
    user: User,
    payload: LetterCreateRequest,
) -> Letter:
    # 1️⃣ 현재 최대 letter_number 조회
    last_number = (
        db.query(func.max(Letter.letter_number))
        .filter(Letter.user_id == user.id)
        .scalar()
    )

    next_number = (last_number or 0) + 1

    letter = Letter(
        user_id=user.id,
        letter_number=next_number,
        writer_nickname=payload.writer_nickname,
        content=payload.content,
        ornament_shape=payload.ornament_shape,
        ornament_color=payload.ornament_color,
        password_for_edit=hash_password(payload.password_for_edit)
        if payload.password_for_edit
        else None,
    )

    db.add(letter)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # 이론상 거의 안 나지만, 동시성 최종 방어
        raise AppException(
            code=ErrorCodes.LETTER_NUMBER_CONFLICT,
            message="잠시 후 다시 시도해주세요.",
        )

    db.refresh(letter)
    return letter


def get_user_letters_paginated(
    *,
    db: Session,
    userid: str,
    limit: int,
    offset: int,
):
    # 1) 유저 확인
    user = db.query(User).filter(User.userid == userid).first()
    if not user:
        raise AppException(
            code=ErrorCodes.USER_NOT_FOUND,
            message="User not found",
        )

    # 2) 편지 조회 (+1로 has_next 판단)
    letters = (
        db.query(Letter)
        .filter(
            Letter.user_id == user.id,
            Letter.is_deleted == False,
        )
        .order_by(Letter.created_at)
        .limit(limit + 1)
        .offset(offset)
        .all()
    )

    has_next = len(letters) > limit
    letters = letters[:limit]

    return {
        "letters": letters,
        "limit": limit,
        "offset": offset,
        "has_next": has_next,
    }