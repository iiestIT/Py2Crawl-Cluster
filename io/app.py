from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from utils.body import ToScrape
from utils.check_envs import check_envs
from config import BaseConfig as bconf
import aioredis
import uvicorn


app = FastAPI()


@app.on_event("startup")
async def startup():
    await check_envs()


@app.post("/to-scrape")
async def to_scrape(items: ToScrape):
    redis = await aioredis.create_redis(f"redis://{bconf.REDIS_HOSTNAME}:{bconf.REDIS_PORT}/0", encoding="utf-8")
    await redis.publish('controller:new')
    return {
        "msg": f"url {items.url} added to queue"
    }


@app.websocket("/get-data")
async def get_data(ws: WebSocket):
    await ws.accept()
    redis = await aioredis.create_redis(f"redis://{bconf.REDIS_HOSTNAME}:{bconf.REDIS_PORT}/0", encoding="utf-8")
    [ch] = await redis.psubscribe('results:*')
    while True:
        msg = await ch.get()
        try:
            await ws.send_json(msg)
        except (ConnectionClosed, WebSocketDisconnect):
            print(f"{ws} disconnected")
            return

if __name__ == "__main__":
    uvicorn.run(
        app, port=bconf.CONTROLLER_PORT
    )
