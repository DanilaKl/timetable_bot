from aiogram.types import BotCommand


def render_menu() -> list[BotCommand]:
    commands = [
        BotCommand(command='/help',
                   description='Полная информация о командах'),
        BotCommand(command='/register',
                   description='Регистрация или изменение данных о пользователе'),
        BotCommand(command='/know',
                   description='Узнать расписание человека'),
        BotCommand(command='/meet',
                   description='Узнать примерное время встреч для заданных людей'),
    ]

    return commands
