import asyncio
import logging as log

from telegram.bot import main


if __name__ == '__main__':
    log.basicConfig(level="INFO")
    asyncio.run(main())







