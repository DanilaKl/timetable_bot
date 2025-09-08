import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeDefault

from config import TOKEN
from handlers import command_handlers
from handlers import registration_handlers
from keyboards import menu_keys
from databases import redis_client


async def main() -> None:
    bot = Bot(TOKEN)
    dp = Dispatcher(storage=redis_client.get_storage())

    dp.include_router(registration_handlers.router)
    dp.include_router(command_handlers.router)

    await bot.set_my_commands(menu_keys.render_menu(), BotCommandScopeDefault())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.info("Serever started")
    asyncio.run(main=main())
