from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def _():
    return {
        "response": "this is the root of the fastAPI API"
    }

