# app/core/redis.py
import redis
from app.core.config import settings

# decode_responses=True → str로 주고받기 (bytes X)
redis_client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)
