import pytest

from api.__main__ import setup_server

@pytest.fixture(scope="class")
def app():
    app = setup_server()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture(scope="class")
def client(app):
    yield app.test_client()


@pytest.mark.usefixtures("client")
class TestApp:
    def test_items(self, client):
        resp = client.get("/items")
        __import__('pdb').set_trace()
        pass

