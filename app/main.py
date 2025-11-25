from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.capsule import router as capsule_router
from app.api.letters import router as letters_router
from app.api.public import router as public_router
from app.core.config import settings

app = FastAPI()


app.include_router(auth_router)
app.include_router(capsule_router)
app.include_router(letters_router)
app.include_router(public_router)


@app.get("/ping")
def ping():
    return {"message": "pong"}