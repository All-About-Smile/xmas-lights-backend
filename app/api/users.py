from typing import Annotated
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.responses import CommonResponse
from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user_schema import UserResponse, UserUpdateRequest
from app.core.exceptions import AppException, ErrorCodes

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
