from flask import Blueprint

from core.lib import items, item

bp = Blueprint("/items", __name__)

@bp.get("/items")
def get():
    return {
        "self": "https://api.spokanepython.com/flask/items/",
        "items": [
            f"https://api.spokanepython.com/flask/item/{i}"
            for i in items.get()
        ]
    }

@bp.post("/items")
def post(name, description, timestamp=None, done=False):
    items.add(item.new(name, description, timestamp, done))
    return "", 201


@bp.delete("/items")
def delete():
    items.clear()
    return "", 204
