from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

WEEK_LABELS = [
    'понедельник',
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
    'воскресенье',
]

WEEK_CODE = [
    'mon',
    'tue',
    'wed',
    'thu',
    'fri',
    'sat',
    'sun',
]


def render_week_days() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(*[InlineKeyboardButton(
                text=title,
                callback_data='reg_tt'
             ) for title, code in zip(WEEK_LABELS, WEEK_CODE)])
    kb.adjust(1)

    return kb.as_markup()


def render_add_remove_time() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Изменить день', callback_data='change_tt')],
        [
            InlineKeyboardButton(text='Добавить', callback_data='add_tt'),
            InlineKeyboardButton(text='Удалить', callback_data='rem_tt')
        ],
        [InlineKeyboardButton(text='Готово', callback_data='confirm_tt')]
    ])

    return kb


def render_reg_form() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить', callback_data='add_tt'),
            InlineKeyboardButton(text='Удалить', callback_data='rem_tt')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='prev_tt'),
            InlineKeyboardButton(text='Далее', callback_data='next_tt')
        ],
        [InlineKeyboardButton(text='Закончить', callback_data='confirm_tt')]
    ])

    return kb
