import redis.asyncio as redis
import os

# redis.cache is thread safe and manages connection pool internally
# create one client and reuse it across all request

cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True # return str instead of bytes
)

CACHE_TTL = 3600

async def get_cached_url(code: str) -> str| None:
    return await cache.get(f"url:{code}")

async def set_cached_url(code:str, original_url: str):
    await cache.setex(f"url: {code}", CACHE_TTL, original_url)

async def increment_clicks(code: str)->int:
    # increment is atomic - safe with 10000 request
    return await cache.incr(f"clicks:{code}")


async def get_clicks_count(code: str) -> str:
    count = await cache.get(f"clicks:{code}")
    return int(count) if count else 0