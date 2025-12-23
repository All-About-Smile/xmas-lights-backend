from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.letter_batch_service import encrypt_existing_letters

router = APIRouter(prefix="/admin", tags=["Admin"])

DBSession = Annotated[Session, Depends(get_db)]


@router.post("/encrypt-letters")
def encrypt_letters_batch(db: DBSession):
    return encrypt_existing_letters(db)
