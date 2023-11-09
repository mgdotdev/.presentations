from cherrypy.test.helper import CPWebCase
from api.__main__ import setup_server

class TestApp(CPWebCase):
    setup_server = staticmethod(setup_server)
    def test_app(self):
        self.getPage("/items", method="OPTIONS")
