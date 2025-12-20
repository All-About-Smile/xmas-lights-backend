# app/services/timecheck.py
from datetime import datetime

from app.core.config import settings
from app.core.time import now_kst, kst_midnight

DEFAULT_TIME_CAPSULE_OPEN_AT = kst_midnight(2025, 12, 25)


def get_time_capsule_open_at() -> datetime:
    """
    타임캡슐 개봉 기준 시각 (KST)
    """
    return settings.TIME_CAPSULE_OPEN_AT or DEFAULT_TIME_CAPSULE_OPEN_AT


def is_time_capsule_open(now: datetime | None = None) -> bool:
    """
    편지 개봉 가능 여부 (KST 기준)
    """
    if now is None:
        now = now_kst()

    return now >= get_time_capsule_open_at()