# app/services/letter_service.py

from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.exceptions import AppException, ErrorCodes
from app.core.security import hash_password, verify_password
from app.db.models.letter import Letter
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.letter_schema import (LetterCreateRequest,
                                       LetterPasswordRequest,
                                       LetterUpdateRequest)
from app.services.timecheck import is_time_capsule_open

router = APIRouter(prefix="/users", tags=["users"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.constants.default_letter import DEFAULT_LETTER
from app.core.deps import get_current_user
from app.core.exceptions import AppException, ErrorCodes
from app.db.models.letter import Letter
from app.db.models.user import User
from app.db.session import get_db


def create_default_letter_for_user(
    *,
    db: Session,
    user: User,
) -> Letter:
    if is_time_capsule_open():
        raise AppException(
            code=ErrorCodes.LETTER_LOCKED_UNTIL_XMAS,
            message="Letters can only be created before Christmas.",
        )

    default_password = DEFAULT_LETTER.get("password")
    if not default_password:
        raise AppException(
            code=ErrorCodes.INVALID_PASSWORD,
            message="Default letter password is missing",
        )

    last_number = (
        db.query(func.max(Letter.letter_number))
        .filter(Letter.user_id == user.id)
        .scalar()
    )
    next_number = (last_number or 0) + 1

    letter = Letter(
        user_id=user.id,
        letter_number=next_number,
        writer_nickname=DEFAULT_LETTER["writer_nickname"],
        content=DEFAULT_LETTER["content"],
        ornament_shape=DEFAULT_LETTER["ornament_shape"],
        ornament_color=DEFAULT_LETTER["ornament_color"],
        password_for_edit=hash_password(default_password),
    )
    db.add(letter)
    db.flush()
    print("check")
    return letter


def create_letter(
    db: Session,
    *,
    user: User,
    payload: LetterCreateRequest,
) -> Letter:
    if is_time_capsule_open():
        raise AppException(
            code=ErrorCodes.LETTER_LOCKED_UNTIL_XMAS,
            message="Letters can only be created before Christmas.",
        )

    # 1) 현재 최대 letter_number 조회
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


def get_letter_detail_for_user(
    *,
    db: Session,
    userid: str,
    letter_number: int,
    current_user: User,
) -> Letter:
    if current_user.userid != userid:
        raise AppException(
            code=ErrorCodes.PERMISSION_DENIED,
            message="You do not have permission to access this letter.",
        )

    letter = (
        db.query(Letter)
        .filter(
            Letter.user_id == current_user.id,
            Letter.letter_number == letter_number,
            Letter.is_deleted == False,
        )
        .first()
    )

    if not letter:
        raise AppException(
            code=ErrorCodes.LETTER_NOT_FOUND,
            message="Letter not found",
        )

    if not is_time_capsule_open():
        raise AppException(
            code=ErrorCodes.LETTER_LOCKED_UNTIL_XMAS,
            message="This letter can be opened on Christmas.",
        )

    return letter


def get_letter_for_edit(
    *,
    db: Session,
    userid: str,
    letter_number: int,
    payload: LetterPasswordRequest,
) -> Letter:
    user = db.query(User).filter(User.userid == userid).first()
    if not user:
        raise AppException(
            code=ErrorCodes.USER_NOT_FOUND,
            message="User not found",
        )

    letter = (
        db.query(Letter)
        .filter(
            Letter.user_id == user.id,
            Letter.letter_number == letter_number,
            Letter.is_deleted == False,
        )
        .first()
    )

    if not letter:
        raise AppException(
            code=ErrorCodes.LETTER_NOT_FOUND,
            message="Letter not found",
        )

    if not letter.password_for_edit or not verify_password(
        payload.password,
        letter.password_for_edit,
    ):
        raise AppException(
            code=ErrorCodes.INVALID_PASSWORD,
            message="Invalid password",
        )

    return letter


def update_letter_for_user(
    *,
    db: Session,
    userid: str,
    letter_number: int,
    payload: LetterUpdateRequest,
) -> None:
    if is_time_capsule_open():
        raise AppException(
            code=ErrorCodes.LETTER_LOCKED_UNTIL_XMAS,
            message="Letters can only be updated before Christmas.",
        )

    user = db.query(User).filter(User.userid == userid).first()
    if not user:
        raise AppException(
            code=ErrorCodes.USER_NOT_FOUND,
            message="User not found",
        )

    letter = (
        db.query(Letter)
        .filter(
            Letter.user_id == user.id,
            Letter.letter_number == letter_number,
            Letter.is_deleted == False,
        )
        .first()
    )

    if not letter:
        raise AppException(
            code=ErrorCodes.LETTER_NOT_FOUND,
            message="Letter not found",
        )

    if not letter.password_for_edit or not verify_password(
        payload.password,
        letter.password_for_edit,
    ):
        raise AppException(
            code=ErrorCodes.INVALID_PASSWORD,
            message="Invalid password",
        )

    if payload.writer_nickname is not None:
        letter.writer_nickname = payload.writer_nickname
    if payload.content is not None:
        letter.content = payload.content
    if payload.ornament_shape is not None:
        letter.ornament_shape = payload.ornament_shape
    if payload.ornament_color is not None:
        letter.ornament_color = payload.ornament_color

    db.commit()


def delete_letter_for_user(
    *,
    db: Session,
    userid: str,
    letter_number: int,
    payload: LetterPasswordRequest,
) -> None:
    if is_time_capsule_open():
        raise AppException(
            code=ErrorCodes.LETTER_LOCKED_UNTIL_XMAS,
            message="Letters can only be deleted before Christmas.",
        )

    user = db.query(User).filter(User.userid == userid).first()
    if not user:
        raise AppException(
            code=ErrorCodes.USER_NOT_FOUND,
            message="User not found",
        )

    letter = (
        db.query(Letter)
        .filter(
            Letter.user_id == user.id,
            Letter.letter_number == letter_number,
            Letter.is_deleted == False,
        )
        .first()
    )

    if not letter:
        raise AppException(
            code=ErrorCodes.LETTER_NOT_FOUND,
            message="Letter not found",
        )

    if not letter.password_for_edit or not verify_password(
        payload.password,
        letter.password_for_edit,
    ):
        raise AppException(
            code=ErrorCodes.INVALID_PASSWORD,
            message="Invalid password",
        )

    letter.is_deleted = True
    db.commit()
