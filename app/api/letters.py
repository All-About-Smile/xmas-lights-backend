from fastapi import APIRouter

router = APIRouter(prefix="/letters", tags=["Letters"])


@router.get("/ping")
def letters_ping():
    return {"message": "letters router ready"}
