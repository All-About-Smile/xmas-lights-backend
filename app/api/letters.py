from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.exceptions import AppException, ErrorCodes
from app.core.responses import CommonResponse
from app.db.models.letter import Letter
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.letter_schema import (LetterCreateRequest,
                                       LetterDetailResponse, LetterListItem,
                                       LetterListResponse)
from app.services.letter_service import (create_letter,
                                         get_user_letters_paginated)

router = APIRouter(prefix="/users", tags=["Letters"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


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