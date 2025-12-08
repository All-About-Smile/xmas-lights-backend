# app/core/timecheck.py
from datetime import datetime


def is_capsule_open(open_at: datetime) -> bool:
    """
    타임캡슐이 열릴 수 있는 날짜인지 확인하는 함수.
    """
    now = datetime.utcnow()
    return now >= open_at


def remaining_time(open_at: datetime) -> str:
    """
    열리기까지 얼마나 남았는지 문자열로 반환.
    """
    now = datetime.utcnow()
    diff = open_at - now

    if diff.total_seconds() <= 0:
        return "Opened"

    days = diff.days
    hours = diff.seconds // 3600

    return f"{days} days {hours} hours left"
