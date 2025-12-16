from fastapi import APIRouter

from app.services.letter_service import create_letter

router = APIRouter(prefix="/users", tags=["Letters"])


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
from app.schemas.letter_schema import LetterCreateRequest, LetterDetailResponse, LetterList

router = APIRouter(prefix="/users", tags=["users"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
from app.db.models.letter import Letter


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
        "items": [LetterList.model_validate(l) for l in letters],
        "limit": limit,
        "offset": offset,
        "has_next": has_next,
    }

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

    return CommonResponse(
        data=LetterDetailResponse.model_validate(letter)
    )

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


@router.get("/ping")
def letters_ping():
    return {"message": "letters router ready"}
