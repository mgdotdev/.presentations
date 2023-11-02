import cherrypy

from .v1 import API

CONFIG = {
    "/": {
        "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
    }
}


def setup_server():
    cherrypy.tree.mount(root=API(), script_name="/", config=CONFIG)


def main():
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    setup_server()
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    main()
