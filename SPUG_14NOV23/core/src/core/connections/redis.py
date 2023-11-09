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


class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class ImmutableDescriptor:
    def __set__(self, *_):
        raise AttributeError(f"descriptors for {self.__class__} can't be set")

    def __delete__(self, *_):
        raise AttributeError(
            f"descriptors for {self.__class__} can't be deleted"
        )


class RedisDescriptor(Singleton, ImmutableDescriptor):
    def __get__(self, *_) -> redis.Redis:
        return redis.Redis(
            connection_pool=getattr(self, "_pool"),
        )


class RedisDatabase(RedisDescriptor):
    _pool = pool_factory(db=APP_SETTINGS.REDIS_DEFAULT)



class Redis(Singleton):
    db = RedisDatabase()

