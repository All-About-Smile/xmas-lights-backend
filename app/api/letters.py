from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.exceptions import AppException, ErrorCodes
from app.core.responses import CommonResponse
from app.core.security import verify_password
from app.core.time import kst_midnight, now_kst
from app.db.models.letter import Letter
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.letter_schema import (
    LetterCreateRequest,
    LetterEditResponse,
    LetterPasswordRequest,
    LetterDetailResponse,
    LetterListItem,
    LetterListResponse,
    LetterUpdateRequest,
)
from app.services.letter_service import create_letter, get_user_letters_paginated
from app.services.timecheck import is_time_capsule_open

router = APIRouter(prefix="/users", tags=["Letters"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

'''
[읽기 – 주인 전용]
GET /users/{userid}/letters/{letter_number}

[수정 – 작성자 전용]
GET    /users/{userid}/letters/{letter_number}/edit
PATCH  /users/{userid}/letters/{letter_number}
DELETE /users/{userid}/letters/{letter_number}
'''


@router.get("/{userid}/letters", response_model=CommonResponse[LetterListResponse])
def read_user_letters(
    userid: str,
    db: DBSession,
    limit: int = Query(8, ge=1, le=20),
    offset: int = Query(0, ge=0),
):
    result = get_user_letters_paginated(
        db=db,
        userid=userid,
        limit=limit,
        offset=offset,
    )

    data = LetterListResponse(
        items=[LetterListItem.model_validate(l) for l in result["letters"]],
        limit=result["limit"],
        offset=result["offset"],
        has_next=result["has_next"],
    )

    return CommonResponse(data=data)


@router.post(
    "/{userid}/letters",
    response_model=CommonResponse[LetterDetailResponse],
)
def create_user_letter(
    userid: str,
    payload: LetterCreateRequest,
    db: DBSession,
):
    user = db.query(User).filter(User.userid == userid).first()
    if not user:
        raise AppException(
            code=ErrorCodes.USER_NOT_FOUND,
            message="존재하지 않는 사용자입니다.",
        )

    letter = create_letter(db=db, user=user, payload=payload)

    return CommonResponse(data=LetterDetailResponse.model_validate(letter))

@router.get(
    "/{userid}/letters/{letter_number}",
    response_model=CommonResponse[LetterDetailResponse],
)
def read_letter_detail(
    userid: str,
    letter_number: int,
    db: DBSession,
    current_user: CurrentUser,  # 로그인 필수
):
    # 1️) userid 주인 확인
    if current_user.userid != userid:
        raise AppException(
            code=ErrorCodes.PERMISSION_DENIED,
            message="You do not have permission to access this letter.",
        )

    # 2️) 편지 조회
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

    # 3️) 크리스마스 잠금 (KST 기준)
    if not is_time_capsule_open():
        raise AppException(
            code=ErrorCodes.LETTER_LOCKED_UNTIL_XMAS,
            message="This letter can be opened on Christmas.",
        )

    # 4️) 응답
    return CommonResponse(
        data=LetterDetailResponse.model_validate(letter)
    )

@router.post(
    "/{userid}/letters/{letter_number}/edit",
    response_model=CommonResponse[LetterEditResponse],
)
def read_letter_for_edit(
    userid: str,
    letter_number: int,
    payload: LetterPasswordRequest,
    db: DBSession,
):
    # 1️) 유저 확인
    user = db.query(User).filter(User.userid == userid).first()
    if not user:
        raise AppException(
            code=ErrorCodes.USER_NOT_FOUND,
            message="User not found",
        )

    # 2️) 편지 조회
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

    # 3️) 비밀번호 검증
    if not letter.password_for_edit or not verify_password(
        payload.password,
        letter.password_for_edit,
    ):
        raise AppException(
            code=ErrorCodes.INVALID_PASSWORD,
            message="Invalid password",
        )

    return CommonResponse(
        data=LetterEditResponse.model_validate(letter)
    )

    
@router.patch(
    "/{userid}/letters/{letter_number}",
    response_model=CommonResponse[None],
)
def update_letter(
    userid: str,
    letter_number: int,
    payload: LetterUpdateRequest,
    db: DBSession,
):
    # 1️) 유저 확인
    user = db.query(User).filter(User.userid == userid).first()
    if not user:
        raise AppException(
            code=ErrorCodes.USER_NOT_FOUND,
            message="User not found",
        )

    # 2️) 편지 조회
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

    # 3️) 비밀번호 검증
    if not letter.password_for_edit or not verify_password(
        payload.password,
        letter.password_for_edit,
    ):
        raise AppException(
            code=ErrorCodes.INVALID_PASSWORD,
            message="Invalid password",
        )

    # 4️) 수정 반영
    if payload.content is not None:
        letter.content = payload.content
    if payload.ornament_shape is not None:
        letter.ornament_shape = payload.ornament_shape
    if payload.ornament_color is not None:
        letter.ornament_color = payload.ornament_color

    db.commit()

    return CommonResponse(data=None)

@router.delete(
    "/{userid}/letters/{letter_number}",
    response_model=CommonResponse[None],
)
def delete_letter(
    userid: str,
    letter_number: int,
    payload: LetterPasswordRequest,
    db: DBSession,
):
    # 1️) 유저 확인
    user = db.query(User).filter(User.userid == userid).first()
    if not user:
        raise AppException(
            code=ErrorCodes.USER_NOT_FOUND,
            message="User not found",
        )

    # 2️) 편지 조회
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

    # 3️) 비밀번호 검증
    if not letter.password_for_edit or not verify_password(
        payload.password,
        letter.password_for_edit,
    ):
        raise AppException(
            code=ErrorCodes.INVALID_PASSWORD,
            message="Invalid password",
        )

    # 4️) Soft Delete
    letter.is_deleted = True
    db.commit()

    return CommonResponse(data=None)
    
    
def get_letters_by_user_id(db: Session, user_id: int):
    return (
        db.query(Letter)
        .filter(
            Letter.user_id == user_id,
            Letter.is_deleted.is_(False),
        )
        .order_by(desc(Letter.created_at))
        .all()
    )
