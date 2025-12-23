from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_crypto_service
from app.db.models.letter import Letter
from app.db.session import get_db

router = APIRouter(prefix="/admin/letters", tags=["Admin"])

DBSession = Annotated[Session, Depends(get_db)]


@router.post("/encrypt-existing")
def encrypt_existing_letters(
    db: DBSession,
):
    crypto = get_crypto_service()

    letters = db.query(Letter).filter(~Letter.content.startswith("gAAAAA")).all()

    updated = 0

    for letter in letters:
        letter.content = crypto.encrypt(letter.content)
        updated += 1

    db.commit()

    return {
        "total": len(letters),
        "encrypted": updated,
    }
