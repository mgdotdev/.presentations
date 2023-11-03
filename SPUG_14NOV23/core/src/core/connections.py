import functools

from core.settings import APP_SETTINGS

import redis

pool_factory = functools.partial(
    redis.ConnectionPool,
    host=APP_SETTINGS.REDIS_HOST,
    port=APP_SETTINGS.REDIS_PORT,
    password=APP_SETTINGS.REDIS_PASSWORD,
    decode_responses=True,
)

REDIS = redis.Redis(connection_pool=pool_factory(db=1))

