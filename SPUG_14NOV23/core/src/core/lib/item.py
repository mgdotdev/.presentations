import uuid
import json
import datetime

from core.connections import REDIS


def new(name, description, timestamp=None, done=False):
    item_id = uuid.uuid4().hex

    timestamp = (
        timestamp or
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    return {
        item_id: {
            "name": name,
            "description": description,
            "timestamp": timestamp,
            "done": done,
        }
    }


def update(item_id, values, redis=REDIS):
    val = json.loads(redis.db.get(item_id))
    val.update(values)
    redis.db.set(item_id, json.dumps(val))


def get(item_id, redis=REDIS):
    val = json.loads(redis.db.get(item_id))
    return {item_id: val}
