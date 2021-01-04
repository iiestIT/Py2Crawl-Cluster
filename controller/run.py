from utils.queue import main
from utils.logger import LOGGER
import asyncio


async def run():
    await asyncio.gather(
        main()
    )

if __name__ == "__main__":
    LOGGER.info("Initialise controller...")
    asyncio.run(run())
