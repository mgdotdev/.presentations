from gunicorn.app.base import BaseApplication
from flask import Flask


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

    @app.route("/")
    def hello():
        return "Hello World!"

    StandaloneApplication(app, conf).run()


if __name__ == "__main__":
    main()
