from utils.queue import main
from utils.logger import LOGGER
import asyncio


async def run():
    await asyncio.gather(
        main("1"),
        main("2"),
        main("3"),
        main("4")
    )

if __name__ == "__main__":
    LOGGER.info("Initialise controller...")
    asyncio.run(run())
