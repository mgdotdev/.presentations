from fastapi import APIRouter, status

from core.lib import items, item

router = APIRouter(prefix="/items")

@router.get("/")
def _():
    return {
        "self": "https://api.spokanepython.com/fastapi/items/",
        "items": [
            f"https://api.spokanepython.com/fastapi/item/{i}"
            for i in items.get()
        ]
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
def _(name, description, timestamp=None, done=False):
    items.add(item.new(name, description, timestamp, done))


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def _():
    items.clear()
