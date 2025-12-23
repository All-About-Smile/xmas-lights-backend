from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.crypto import CryptoService
from app.db.models.user import User
from app.db.session import get_db

# Authorization: Bearer <token>
bearer_scheme = HTTPBearer()

DBSession = Annotated[Session, Depends(get_db)]
AuthCredentials = Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]


def get_current_user(
    credentials: AuthCredentials,
    db: DBSession,
) -> User:
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception
    except JWTError as err:
        raise credentials_exception from err

    user = db.get(User, int(user_id))
    if user is None:
        raise credentials_exception

    return user


@lru_cache
def get_crypto_service() -> CryptoService:
    return CryptoService(settings.LETTER_CRYPTO_KEY)
