from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from utils.body import ToScrape
from utils.check_envs import check_envs
from config import BaseConfig as bconf
import aioredis
import uvicorn
import json
import uuid

app = FastAPI()


@app.on_event("startup")
async def startup():
    await check_envs()


@app.post("/to-scrape")
async def to_scrape(items: ToScrape):
    redis = await aioredis.create_redis(f"redis://{bconf.REDIS_HOSTNAME}:{bconf.REDIS_PORT}/0", encoding="utf-8")
    _id = uuid.uuid4()
    redis.rpush('toscrape:new', json.dumps({
        "url": f"{items.url}",
        "id": f"{_id}",
        "scope": 1 if items.scope == True else 0
    }))
    redis.close()
    await redis.wait_closed()
    return {
        "url": f"{items.url}",
        "id": f"{_id}"
    }


@app.websocket("/get-data")
async def get_data(ws: WebSocket):
    await ws.accept()
    redis = await aioredis.create_redis(f"redis://{bconf.REDIS_HOSTNAME}:{bconf.REDIS_PORT}/0", encoding="utf-8")
    [ch] = await redis.psubscribe('results:*')
    while True:
        msg = await ch.get()
        msg = msg[1].decode("utf-8")
        try:
            await ws.send_json(msg)
        except (ConnectionClosed, WebSocketDisconnect):
            return


if __name__ == "__main__":
    uvicorn.run(
        app, port=bconf.CONTROLLER_PORT, host="0.0.0.0"
    )
