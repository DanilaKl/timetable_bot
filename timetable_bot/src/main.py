import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import TOKEN


async def main() -> None:
    bot = Bot(TOKEN)
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.info("Serever started")
    asyncio.run(main=main())
