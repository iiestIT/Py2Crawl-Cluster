from utils.check_envs import check_envs
from config import BaseConfig as bconf
from utils.crawled import check_url
from utils.logger import LOGGER
import aioredis
import json


async def main(t):
    await check_envs()

    redis = await aioredis.create_redis(f"redis://{bconf.REDIS_HOSTNAME}:{bconf.REDIS_PORT}/0", encoding="utf-8")

    while True:
        j = await redis.blpop('toscrape:new')
        j = json.loads(j[1])

        LOGGER.info(f"Controller: {t}")

        check = await check_url(j.get("id"), j.get("url"))

        if check:
            continue

        await redis.rpush('toscrap:available', json.dumps({
            "url": j.get("url"),
            "id": j.get("id"),
            "scope": j.get("scope")
        }))
