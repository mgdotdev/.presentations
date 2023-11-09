from fastapi import APIRouter, status

from core.lib.items import remove
from core.lib.item import get, update

router = APIRouter(prefix="/item")


@router.get("/{item}")
def _(item):
    return {
        "self": f"https://api.spokanepython.com/fastapi/item/{item}",
        "item": get(item)
    }


@router.patch("/{item}", status_code=status.HTTP_204_NO_CONTENT)
def _(item, **kwargs):
    update(item, kwargs)


@router.delete("/{item}", status_code=status.HTTP_204_NO_CONTENT)
def _(item):
    remove(item)
