from fastapi import APIRouter

router = APIRouter(prefix="/capsule", tags=["Capsule"])


@router.get("/ping")
def capsule_ping():
    return {"message": "capsule router ready"}
