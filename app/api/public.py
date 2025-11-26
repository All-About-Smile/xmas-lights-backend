from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["Public"])

@router.get("/ping")
def public_ping():
    return {"message": "public router ready"}
