from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message

from services import timetable_service as tt_service
from services import prettify_print_service as pp_service

router = Router()


@router.message(Command(commands=['know']))
async def get_timetable(message: Message, command: CommandObject) -> None:
    text = 'Что-то пошло не так, не получилось найти подходящего расписания'
    if not command.args and message.from_user:
        timetable = await tt_service.get_user_timetable(user_id=message.from_user.id)
        text = f'Расписание: {pp_service.prettify_timetable(timetable)}'
    elif command.args:
        user_name = command.args.lstrip('@')
        timetable = await tt_service.get_user_timetable(user_name=user_name)
        text = f'Расписание: {pp_service.prettify_timetable(timetable)}'

    await message.answer(text=text)


@router.message(Command(commands=['meet']))
async def get_meeting(message: Message, command: CommandObject) -> None:
    if command.args:
        user_names = [user_mention.lstrip('@') for user_mention in command.args.split()]
        meeting_time = await tt_service.request_meeting(user_names)
        text = f'Возможное время встречи: {pp_service.prettify_timetable(meeting_time)}'
    else:
        timetable = await tt_service.get_user_timetable(
            user_id=message.from_user.id)  # type: ignore
        text = (f'Так как параметрыне не были переданы , '
                f'показано ваше расписание: {pp_service.prettify_timetable(timetable)}')

    await message.answer(text=text)


@router.message(CommandStart)
async def init_user(message: Message) -> None:
    if message.from_user:
        await tt_service.init_user(message.from_user.id,
                                   message.from_user.username)  # type: ignore
