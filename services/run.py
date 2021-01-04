from PySide2.QtWidgets import QApplication
from Py2Web.utils.xvfb import VirtualDisplay
from Py2Crawl.utils import LOGGER
from utils.spider import main
import asyncio

VD = VirtualDisplay()


async def run():
    await asyncio.gather(
        main(app, "1"),
        main(app, "2"),
        main(app, "3"),
        main(app, "4")
    )


if __name__ == "__main__":
    LOGGER.info("Initialise services...")
    VD.init_xvfb()
    app = QApplication([])
    asyncio.run(run())
