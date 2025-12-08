from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.capsule import router as capsule_router
from app.api.letters import router as letters_router
from app.api.public import router as public_router
from app.core.config import settings

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public_router)
app.include_router(auth_router)
app.include_router(capsule_router)
app.include_router(letters_router)
app.include_router(public_router)


@app.get("/ping")
def ping():
    return {"message": "pong"}