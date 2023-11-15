from urllib.parse import urlencode

from cherrypy.test.helper import CPWebCase
from api.__main__ import setup_server

import json

class TestApp(CPWebCase):
    setup_server = staticmethod(setup_server)
    def test_root(self):
        self.getPage("/")
        assert json.loads(self.body) == {
            "response":"this is the root of the CherryPy API"
        }

    def test_items(self):

        self.getPage("/items", method="DELETE")

        assert self.status_code == 204

        data = dict(
            name="this",
            description="that"
        )

        self.getPage("/items", method="POST", body=urlencode(data))

        assert self.status_code == 201

        self.getPage("/items")

        assert self.status_code == 200

        item = json.loads(self.body)["items"].pop()
        item_id = item.split("/").pop()

        self.getPage(f"/item/{item_id}")
        _, v = json.loads(self.body)["item"].popitem()

        for key in data.keys():
            assert data[key] == v[key]

        self.getPage("/items", method="DELETE")

        assert self.status_code == 204

