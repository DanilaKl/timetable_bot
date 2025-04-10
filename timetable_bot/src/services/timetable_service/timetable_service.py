from datetime import time

from databases import users_mongo_client as client
from .timetable_utils import find_timetable_intersections, construct_timetable


def time_to_minutes(weekday: int, timestamp: time) -> int:
    return (
        weekday * 24 * 60 +
        timestamp.hour * 60 +
        timestamp.minute
    )


async def get_user_timetable(*, user_id: int | None = None,
                             user_name: str | None = None) -> list[tuple]:
    if (not user_id and not user_name) or (user_id and user_name):
        raise ValueError('Must specify user_id or user_name')

    timetable_key = 'timetable'
    if user_id:
        user_data = await client.get_user_fields_by_id(user_id, fields=[timetable_key])
    elif user_name:
        user_data = await client.get_user_fields_by_name(user_name, fields=[timetable_key])

    if not user_data:
        return []

    return user_data[timetable_key]


async def request_meeting(user_names: list[str]) -> list[tuple]:
    timetables = [await get_user_timetable(user_name=user_name) for user_name in user_names]
    intersection = find_timetable_intersections(timetables)

    return intersection


async def init_user(id: int, user_name: str) -> None:
    await client.add_user(id, user_name)


async def register_user(id: int,
                        add_intervals: list[tuple[int, int]],
                        rem_intervals: list[tuple[int, int]]) -> None:
    user_data = await client.get_user_fields_by_id(id, ['timetable'])

    if not user_data:
        raise ValueError('No user with specified id')

    new_timetable = construct_timetable(user_data['timetable'], add_intervals, rem_intervals)

    await client.update_user(id, timetable=new_timetable)

__all__ = [
    'time_to_minutes',
    'get_user_timetable',
    'request_meeting',
    'init_user',
    'register_user',
]
