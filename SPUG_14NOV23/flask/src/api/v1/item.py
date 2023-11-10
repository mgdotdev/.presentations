from flask import Blueprint

from core.lib.items import remove
from core.lib.item import get, update

bp = Blueprint("/item", __name__)


@bp.get("/{item}")
def get(item):
    return {
        "self": f"https://api.spokanepython.com/fastapi/item/{item}",
        "item": get(item)
    }


@bp.patch("/{item}")
def patch(item, **kwargs):
    update(item, kwargs)
    return "", 204



@bp.delete("/{item}")
def delete(item):
    remove(item)
    return "", 204
