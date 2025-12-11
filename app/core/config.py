# app/core/config.py
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "local"
    PROJECT_NAME: str = "TimeCapsule-Backend"
    API_V1_STR: str = "/api"

    # DB는 마지막 단계에서 설정
    DATABASE_URL: str

    # ── JWT ──
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1일
    
    # ── Redis ──
    REDIS_URL: str = "redis://localhost:6379/0"
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",  # 혹시 .env에 정의 안 한 필드 있어도 무시
    )


def get_settings():
    # ENV 환경 변수 → 없으면 .env.* 파일 안의 ENV 값이 적용됨
    env = os.getenv("ENV", ".env.local").strip()

    # ENV에 따라 env 파일 선택
    env_map = {
        "prod": ".env",
        "dev": ".env.dev",
        "local": ".env.local",
    }

    env_file = env_map.get(env, ".env.local")

    # 동적으로 env_file 지정
    class _Settings(Settings):
        model_config = SettingsConfigDict(
            env_file=env_file,
            env_file_encoding="utf-8",
            extra="ignore",
        )

    return _Settings()


settings = get_settings()
