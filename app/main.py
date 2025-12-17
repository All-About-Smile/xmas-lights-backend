from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.letters import router as letters_router
from app.api.users import router as users_router
from app.api.public import router as public_router
from app.core.config import settings
from app.core.exception_handlers import app_exception_handler, generic_exception_handler
from app.core.exceptions import AppException

app = FastAPI(title=settings.PROJECT_NAME)

# ── Exception Handlers ──
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# ── CORS ──
if settings.cors_origins_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Date"],
    )

# ── Routers ──
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(letters_router)
app.include_router(public_router)


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.get("/env")
def read_env():
    return {"env": settings.ENV}
