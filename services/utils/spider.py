from Py2Crawl.py2crawl import Py2Crawl
from Py2Crawl.spider import Py2CrawlSpider
from Py2Crawl.http.methods import Py2CrawlMethods
from Py2Crawl.utils import LOGGER
from config import BaseConfig as bconf
from utils.check_envs import check_envs
from utils.links import LinkParser
import aioredis
import json


async def main(app):
    await check_envs()

    redis = await aioredis.create_redis(f"redis://{bconf.REDIS_HOSTNAME}:{bconf.REDIS_PORT}/0", encoding="utf-8")

    while True:
        LOGGER.info("wait for urls ... ")  # TODO: remove line
        target = await redis.blpop('toscrap:available')
        target = json.loads(target[1])

        async def test_func(response):
            links = await LinkParser(str(response.content), str(response.url)).links()
            if target.get("scope") == 1:
                [await redis.rpush('toscrape:new', json.dumps({"url": i, "id": target.get("id")})) for i in links[1]]
            await redis.publish('results:1', str({
                "links": links[0],
                "content": response.content,
                "url": response.url,
                "cookies": response.cookies
            }))

        crawler = Py2Crawl()
        spider = Py2CrawlSpider(
            start_urls=[target.get("url")],
            start_urls_method=Py2CrawlMethods.PW_GET,
            callback=test_func,
            q_app=app,
            start_script="1+1"
        )
        await crawler.crawl(spider)
