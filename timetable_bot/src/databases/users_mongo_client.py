import motor.motor_asyncio

from typing import Any

from config import (MONGO_DB_NAME, MONGO_USER,
                    MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_COLLECTION)


uri = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}'
users: motor.motor_asyncio.AsyncIOMotorCollection = (
    motor.motor_asyncio.AsyncIOMotorClient(uri)[MONGO_DB_NAME][MONGO_COLLECTION]
)


async def add_user(id: int, user_name: str) -> None:
    insertion_doc: dict[str, Any] = {
        '$setOnInsert': {
            '_id': id,
            'name': user_name,
            'timetable': [],
            'registration_finished': False
        }
    }

    await users.update_one({'_id': id}, insertion_doc, upsert=True)


async def update_user(id: int, *,
                      user_name: str | None = None,
                      timetable: list[tuple] | None = None) -> None:
    update_doc: dict[str, Any] = {'$set': {}}
    if user_name:
        update_doc['$set']['name'] = user_name

    if timetable:
        update_doc['$set']['timetable'] = timetable
        update_doc['$set']['registration_finished'] = True

    await users.update_one({'_id': id}, update=update_doc)


async def get_user_fields_by_id(user_id: int, fields: list[str] | None = None) -> dict | None:
    """Get specific fields from user document. Return full record if fields weren't specified"""
    if fields:
        return await users.find_one({'_id': user_id}, projection=fields)

    return await users.find_one({'_id': user_id})


async def get_user_fields_by_name(user_name: str, fields: list[str] | None = None) -> dict | None:
    """Get specific fields from user document. Return all fields if fields weren't specified"""
    if fields:
        return await users.find_one({'name': user_name}, projection=fields)

    return await users.find_one({'name': user_name})


__all__ = [
    'add_user',
    'update_user',
    'get_user_fields_by_id',
    'get_user_fields_by_name',
]
