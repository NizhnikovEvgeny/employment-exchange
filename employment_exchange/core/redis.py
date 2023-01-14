from typing import AsyncIterator
import redis

from core.config import REDIS_URL

DEFAULT_KEY_PREFIX = "emp"


# class Keys:
#     """Methods to generate key names for Redis data structures."""

#     def __init__(self, prefix: str = DEFAULT_KEY_PREFIX):
# self.prefix = prefix


async def initialize_redis():
    return redis.from_url(REDIS_URL, decode_responses=True)
