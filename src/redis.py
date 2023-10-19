from datetime import timedelta
from pydantic import BaseModel
from redis.asyncio import Redis

redis_client: Redis = None  # type: ignore


class RedisData(BaseModel):
    key: bytes | str
    value: bytes | str
    ttl: int | timedelta | None = None


async def set_redis_key(redis_data: RedisData, *, is_transaction: bool = False) -> None:
    async with redis_client.pipeline(transaction=is_transaction) as pipe:
        await pipe.set(redis_data.key, redis_data.value)
        if redis_data.ttl:
            await pipe.expire(redis_data.key, redis_data.ttl)

        await pipe.execute()


async def get_by_key(key: str) -> str | None:
    return await redis_client.get(key)


async def delete_by_key(key: str) -> None:
    return await redis_client.delete(key)
