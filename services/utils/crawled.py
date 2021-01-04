from urllib.parse import urlparse
from config import BaseConfig as bconf
import aioredis


async def add_url(_id, url):
    redis = await aioredis.create_redis(f"redis://{bconf.REDIS_HOSTNAME}:{bconf.REDIS_PORT}/0", encoding="utf-8")
    await redis.hset(
        key=f"{_id}",
        field=f"{urlparse(url).netloc}{urlparse(url).path.replace('/', ':')}",
        value=f"{url}"
    )
    redis.close()
    await redis.wait_closed()
