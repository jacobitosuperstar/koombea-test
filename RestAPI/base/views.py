import datetime
from fastapi import APIRouter

from .models import TestResponse


router: APIRouter = APIRouter()


@router.get("/ping/")
def ping() -> TestResponse:
    """Checking the health of the server.
    """
    return TestResponse(now=datetime.datetime.now())
