from fastapi import APIRouter

router = APIRouter(prefix="/letters", tags=["Letters"])


from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.models.letter import Letter


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
