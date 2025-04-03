from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()


@router.message(CommandStart)
async def init_user(message: Message) -> None:
    if message.from_user:
        await message.answer(f'Hello, {message.from_user.username}')
