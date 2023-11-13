import pytest

from copy import deepcopy
from types import SimpleNamespace


import redis as r

from core.connections.redis import pool_factory
from core.lib import item, items


@pytest.fixture(scope="class")
def redis():
    instance = r.Redis(connection_pool=pool_factory(db=2))
    instance.flushall()
    yield SimpleNamespace(db=instance)
    instance.flushall()
    instance.close()


class TestRedis:
    def test_item(self):
        expected = dict(name="a", description="b", timestamp="c", done=False)
        i = item.new(**expected)
        k, v = i.popitem()
        assert len(k) == 32
        assert v == expected


    def test_items(self, redis):
        expected = dict(name="a", description="a", timestamp="a", done=False)
        val = item.new(**expected)
        items.add(deepcopy(val), redis=redis)
        vals = items.get(redis=redis)
        assert vals == list(val)
        k = vals.pop()
        items.remove(k, redis=redis)
        vals = items.get(redis=redis)
        assert vals == []


    def test_update(self, redis):
        expected = dict(name="a", description="a", timestamp="a", done=False)
        val = item.new(**expected)
        items.add(deepcopy(val), redis=redis)
        k = list(val.keys()).pop()
        new = dict(name="b", done=True)
        item.update(k, new, redis=redis)
        expected.update(new)
        ak, actual = item.get(k, redis=redis).popitem()
        assert ak == k
        assert actual == expected

