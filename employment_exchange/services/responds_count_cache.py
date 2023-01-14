from redis import Redis


class RespondsCountCache:
    RESPONDS_COUNT_PREFIX = "job_responds_count"
    EXPIRE_IN_SECONDS = 300

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    @classmethod
    def _responds_count_cache_key(cls, job_id: int) -> str:
        return f"{cls.RESPONDS_COUNT_PREFIX}-{job_id}"

    async def get_responds_count(self, job_id: int):
        return self._redis.get(self._responds_count_cache_key(job_id=job_id))

    async def set_responds_count(self, job_id: int, count: int):
        self._redis.set(name=self._responds_count_cache_key(
            job_id=job_id), value=count, ex=self.EXPIRE_IN_SECONDS)

    async def increment_if_exists(self, job_id: int):
        self._redis.incr(name=self._responds_count_cache_key(job_id=job_id))
