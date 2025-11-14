import asyncio
from functools import wraps
from time import time


def sync_to_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper

def calculate_duration(start_time: float) -> int:
    """
    Возвращает округлённое значение времени
    исполнения запроса в мсек
    """
    return round(time()*1000 - start_time)
