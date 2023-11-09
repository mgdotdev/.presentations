import json

from core.connections import REDIS
from .item import new


ITEMS = "items"


def add(item, redis=REDIS):
    k, v = item.popitem()
    redis.db.set(k, json.dumps(v))
    redis.db.lpush(ITEMS, k)


def remove(item_id, redis=REDIS):
    redis.db.lrem(ITEMS, 1, item_id)
    redis.db.delete(item_id)


def get(redis=REDIS):
    items = redis.db.lrange(ITEMS, 0, -1)
    return items


def clear(redis=REDIS):
    redis.db.flushall()

