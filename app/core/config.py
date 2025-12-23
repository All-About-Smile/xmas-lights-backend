# app/core/config.py
import os
from datetime import datetime
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.time import KST


class Settings(BaseSettings):
    ENV: str = "local"
    PROJECT_NAME: str = "TimeCapsule-Backend"
    API_V1_STR: str = "/api"

    # ── DB ──
    DATABASE_URL: str

    # ── JWT ──
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1일

    # ── Redis ──
    REDIS_URL: str = "redis://localhost:6379/0"
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── Cookie ──
    COOKIE_SECURE: bool = False  # True면 HTTPS에서만 쿠키 전송
    COOKIE_SAMESITE: str = "lax"

    # ── CORS ──
    CORS_ORIGINS: str = ""  # "http://localhost:5173,https://xxx"

    # ── Time Capsule ──
    TIME_CAPSULE_OPEN_AT: datetime | None = None

    # ── Crypto ──
    LETTER_CRYPTO_KEY: str

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """
        CORS_ORIGINS를 콤마(,) 기준으로 split 해서 리스트로 반환
        """
        if not self.CORS_ORIGINS:
            return []
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @field_validator("TIME_CAPSULE_OPEN_AT", mode="before", check_fields=False)
    @classmethod
    def parse_time_capsule_open_at(cls, v):
        if v is None:
            return None

        if isinstance(v, datetime):
            return v

        dt = datetime.fromisoformat(v)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=KST)

        return dt


def get_settings():
    env = os.getenv("ENV", "local").strip()

    env_map = {
        "prod": ".env",
        "dev": ".env.dev",
        "local": ".env.local",
    }

    env_file = env_map.get(env, ".env.local")

    class _Settings(Settings):
        model_config = SettingsConfigDict(
            env_file=env_file,
            env_file_encoding="utf-8",
            extra="ignore",
        )

    return _Settings()


settings = get_settings()
