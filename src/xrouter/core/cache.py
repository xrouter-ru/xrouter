"""Redis cache and rate limiting."""
import json
from typing import Any, Optional

from redis.asyncio import Redis

from xrouter.core.config import settings


class RedisClient:
    """Redis client for caching and rate limiting."""

    def __init__(self, redis: Redis[Any]) -> None:
        """Initialize Redis client.

        Args:
            redis: Redis connection.
        """
        self.redis = redis

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis.

        Args:
            key: Redis key.

        Returns:
            Any: Value from Redis or None if key doesn't exist.
        """
        value = await self.redis.get(settings.get_redis_key(key))
        if value is None:
            return None
        return json.loads(value)

    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None,
    ) -> None:
        """Set value in Redis.

        Args:
            key: Redis key.
            value: Value to store.
            expire: Expiration time in seconds.
        """
        await self.redis.set(
            settings.get_redis_key(key),
            json.dumps(value),
            ex=expire,
        )

    async def delete(self, key: str) -> None:
        """Delete value from Redis.

        Args:
            key: Redis key.
        """
        await self.redis.delete(settings.get_redis_key(key))

    async def increment_rate_limit(self, api_key: str) -> int:
        """Increment rate limit counter.

        Args:
            api_key: API key.

        Returns:
            int: Current rate limit count.
        """
        key = settings.get_rate_limit_key(api_key)
        count: int = await self.redis.incr(key)  # type: ignore
        if count == 1:
            await self.redis.expire(key, 60)  # 1 minute window
        return count

    async def get_rate_limit(self, api_key: str) -> int:
        """Get current rate limit count.

        Args:
            api_key: API key.

        Returns:
            int: Current rate limit count.
        """
        key = settings.get_rate_limit_key(api_key)
        count: Optional[bytes] = await self.redis.get(key)
        return int(count.decode()) if count else 0

    async def cache_get(self, key: str) -> Optional[Any]:
        """Get value from cache.

        Args:
            key: Cache key.

        Returns:
            Any: Value from cache or None if key doesn't exist.
        """
        return await self.get(settings.get_cache_key(key))

    async def cache_set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None,
    ) -> None:
        """Set value in cache.

        Args:
            key: Cache key.
            value: Value to store.
            expire: Expiration time in seconds.
        """
        await self.set(
            settings.get_cache_key(key),
            value,
            expire or settings.CACHE_TTL,
        )

    async def cache_delete(self, key: str) -> None:
        """Delete value from cache.

        Args:
            key: Cache key.
        """
        await self.delete(settings.get_cache_key(key))
