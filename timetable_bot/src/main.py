import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import command_handlers
from handlers import registration_handlers


async def main() -> None:
    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.include_router(registration_handlers.router)
    dp.include_router(command_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.info("Serever started")
    asyncio.run(main=main())
