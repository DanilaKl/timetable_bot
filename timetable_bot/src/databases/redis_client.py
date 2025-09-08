from aiogram.fsm.storage.redis import RedisStorage
from config import REDIS_HOST, REDIS_PORT, REDIS_USER, REDIS_PASSWORD


redis_url = f'redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
storage = RedisStorage.from_url(redis_url)


def get_storage():
    return storage


__all__ = [
    'get_storage',
]
