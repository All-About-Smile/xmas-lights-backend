from datetime import datetime
from app.core.time import now_kst, kst_midnight

TIME_CAPSULE_OPEN_DATE = (2025, 12, 25)


def is_time_capsule_open(now: datetime | None = None) -> bool:
    """
    편지 개봉 가능 여부 (KST 기준)
    """
    if now is None:
        now = now_kst()

    open_at = kst_midnight(*TIME_CAPSULE_OPEN_DATE)
    return now >= open_at
