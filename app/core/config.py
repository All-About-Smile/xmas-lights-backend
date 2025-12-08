# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "TimeCapsule-Backend"
    API_V1_STR: str = "/api"

    # DB는 마지막 단계에서 설정
    DATABASE_URL: str

    # ── JWT ──
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1일

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # 혹시 .env에 정의 안 한 필드 있어도 무시
    )


settings = Settings()
