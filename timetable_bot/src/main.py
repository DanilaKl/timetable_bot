import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import TOKEN


dp = Dispatcher()


@dp.message(CommandStart)
async def dummy_handler(message: Message) -> None:
    if message.from_user:
        await message.answer(f'Hello, {message.from_user.username}!')


async def main() -> None:
    bot = Bot(TOKEN)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.info("Serever started")
    asyncio.run(main=main())
