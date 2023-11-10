from gunicorn.app.base import BaseApplication
from flask import Flask

from . import v1
from .v1 import items, item


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():
    conf = {
        "bind": "0.0.0.0:8080",
        "workers": 1,
    }
    app = Flask(__name__)

    v1.bp.register_blueprint(items.bp)
    v1.bp.register_blueprint(item.bp)
    app.register_blueprint(v1.bp)

    StandaloneApplication(app, conf).run()


if __name__ == "__main__":
    main()
