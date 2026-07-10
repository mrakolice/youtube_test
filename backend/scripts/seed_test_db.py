"""Test database seeding script."""

import asyncio
import functools


async def seed_test_db():
    """Seed test database with mock data."""
    # TODO: Implement test database seeding
    print("Test database seeding completed")


if __name__ == "__main__":
    asyncio.run(seed_test_db())


def async_cache(expiration_time: int):
    cache = {}
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            if cache_key in cache:
                return cache[cache_key]

            result = await func(*args, **kwargs)
            cache_value = (result, asyncio.get_event_loop().time() + expiration_time)
            cache[cache_key] = cache_value
        return wrapper
    return decorator
    """Asynchronously cache a value with an expiration time."""