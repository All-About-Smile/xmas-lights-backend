from fastapi import APIRouter

router = APIRouter(prefix="/rollingpaper", tags=["Capsule"])


@router.get("/ping")
def rollingpaper_ping():
    return {"message": "rollingpaper router ready"}
