from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import services.timetable_service as tt_service
import services.prettify_print_service as pp_service

from keyboards.registration_keys import render_reg_form
from validators.time_validator import validate_intervals


router = Router()


class RegistationStates(StatesGroup):
    interval_add = State()
    interval_rem = State()


@router.message(Command('register'))
async def start_registration(message: Message, state: FSMContext) -> None:
    await state.set_state(RegistationStates.interval_add)
    await state.set_data({
        'week': 0,
        'adds': [],
        'rems': []})
    await message.answer(
        f'Заполните интервалы свободного времени.\n[{pp_service.prettify_week_day(0)}]:',
        reply_markup=render_reg_form()
    )


@router.callback_query(F.data == "next_tt")
async def goto_next_week_day(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    data['week'] = (data['week'] + 1) % 7
    await state.set_data(data=data)
    if callback.message:
        week_day = pp_service.prettify_week_day(data["week"])
        await callback.message.answer(
            f'Заполните интервалы свободного времени.\n[{week_day}]:',
            reply_markup=render_reg_form()
        )


@router.callback_query(F.data == "prev_tt")
async def goto_prev_week_day(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    data['week'] = (data['week'] - 1) % 7
    await state.set_data(data=data)
    if callback.message:
        week_day = pp_service.prettify_week_day(data["week"])
        await callback.message.answer(
            f'Заполните интервалы свободного времени.\n[{week_day}]:',
            reply_markup=render_reg_form()
        )


@router.callback_query(F.data == "add_tt")
async def add_time_intervals(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(RegistationStates.interval_add)
    if callback.message:
        await callback.message.answer(
            text='Теперь выможете добавлять временной интервал.\n[Пример] 14:00 - 15:30'
        )


@router.callback_query(F.data == "rem_tt")
async def remove_time_intervals(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(RegistationStates.interval_rem)
    if callback.message:
        await callback.message.answer(
            text='Теперь выможете добавлять временной интервал.\n[Пример] 14:00 - 15:30'
        )


@router.message(
    StateFilter(RegistationStates.interval_add, RegistationStates.interval_rem)
)
async def proccess_time_interval(message: Message, state: FSMContext) -> None:
    try:
        start, end = validate_intervals(str(message.text))
    except ValueError as error:
        await message.answer(text=str(error))
        return

    data = await state.get_data()
    weekday = data['week']
    cur_state = await state.get_state()
    if cur_state == RegistationStates.interval_add.state:
        interval_key = 'adds'
    else:
        interval_key = 'rems'
    data[interval_key].append(
        (tt_service.time_to_minutes(weekday, start),
         tt_service.time_to_minutes(weekday, end))
    )
    await state.set_data(data)


@router.callback_query(F.data == "confirm_tt")
async def end_registration(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    await state.clear()
    await tt_service.register_user(callback.from_user.id,
                                   data['adds'],
                                   data['rems'])

    if callback.message:
        await callback.message.answer(text='Ваше расписание сохранено')
