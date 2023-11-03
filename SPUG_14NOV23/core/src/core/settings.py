import os

from types import new_class


def APP_SETTINGS():
    """app settings closure, where settings are cached so that the os env is
    only read once per key, and read lazily."""

    cache = {}

    def __getattr__(_, key):
        return cache.setdefault(key, os.environ[key])

    def __setattr__(*_):
        raise AttributeError(
            "APP_SETTINGS does not support attribute assignment"
        )

    def __delattr__(*_):
        raise RuntimeError("cannot delete attributes from APP_SETTINGS")

    methods = {
        "__getattr__": __getattr__,
        "__setattr__": __setattr__,
        "__delattr__": __delattr__,
    }

    _type = new_class("APP_SETTINGS", exec_body=lambda ns: ns.update(methods))

    return _type()


APP_SETTINGS = APP_SETTINGS()

