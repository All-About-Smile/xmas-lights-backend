from sqlalchemy.orm import Session

from app.core.exceptions import AppException, ErrorCodes
from app.core.security import hash_password
from app.db.models.user import User
from app.schemas.auth_schema import RegisterRequest
from app.services.letter_service import create_default_letter_for_user


def register_user(*, db: Session, payload: RegisterRequest) -> User:
    if db.query(User).filter(User.userid == payload.userid).first():
        raise AppException(
            code=ErrorCodes.USER_ALREADY_EXISTS,
            message="UserID already taken",
        )

    if db.query(User).filter(User.email == payload.email).first():
        raise AppException(
            code=ErrorCodes.USER_ALREADY_EXISTS,
            message="Email already registered",
        )

    password_hash = hash_password(payload.password)
    user = User(
        userid=payload.userid,
        email=payload.email,
        password_hash=password_hash,
    )
    db.add(user)

    db.flush()
    create_default_letter_for_user(
        db=db,
        user=user,
    )
    db.commit()
    db.refresh(user)

    return user
