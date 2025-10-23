import aioredis
from src.config.settings import settings
from src.server_logger import logger


class RedisStore:
    def __init__(self):
        self.redis = None

    async def connection(self):
        redis_url = f"redis://{settings.redis_host}:{settings.redis_port}"
        self.redis = await aioredis.from_url(
            url=redis_url,
            encoding="utf-8",
            decode_responses=True
        )
        logger.info("[Redis] Подключение установлено")

    async def set(self, key: str, value: str, ttl: int | None = None):
        await self.redis.set(key, value, ex=ttl)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        await self.redis.close()
        logger.info("[Redis] Соединение закрыто")


redis_store = RedisStore()
