from fastapi import FastAPI
import uvicorn

from . import v1
from .v1 import items, item

def setup_server():
    app = FastAPI()
    v1.router.include_router(items.router)
    v1.router.include_router(item.router)
    app.include_router(v1.router)
    return app

def main():
    uvicorn.run(setup_server(), host="0.0.0.0", port="8000")


if __name__ == "__main__":
    main()
