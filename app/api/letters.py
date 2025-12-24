from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.exceptions import AppException, ErrorCodes
from app.core.responses import CommonResponse
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
from app.services.letter_service import (
    create_letter,
    delete_letter_for_user,
    get_letter_detail_for_user,
    get_letter_for_edit,
    get_user_letters_paginated,
    update_letter_for_user,
)

router = APIRouter(prefix="/users", tags=["Letters"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

'''
[읽기 - 주인 전용]
GET /users/{userid}/letters/{letter_number}

[수정 - 작성자 전용]
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
        total_count=result["total_count"],
        total_pages=result["total_pages"],
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
    letter = get_letter_detail_for_user(
        db=db,
        userid=userid,
        letter_number=letter_number,
        current_user=current_user,
    )

    return CommonResponse(data=LetterDetailResponse.model_validate(letter))

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
    letter = get_letter_for_edit(
        db=db,
        userid=userid,
        letter_number=letter_number,
        payload=payload,
    )

    return CommonResponse(data=LetterEditResponse.model_validate(letter))

    
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
    update_letter_for_user(
        db=db,
        userid=userid,
        letter_number=letter_number,
        payload=payload,
    )

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
    delete_letter_for_user(
        db=db,
        userid=userid,
        letter_number=letter_number,
        payload=payload,
    )

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
