from datetime import datetime
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")
UTC = ZoneInfo("UTC")


def now_utc() -> datetime:
    return datetime.now(UTC)


def now_kst() -> datetime:
    return datetime.now(KST)


def to_kst(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(KST)


def kst_midnight(year: int, month: int, day: int) -> datetime:
    """
    KST 기준 자정 datetime 생성
    """
    return datetime(year, month, day, 0, 0, 0, tzinfo=KST)
