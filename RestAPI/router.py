from fastapi.routing import APIRouter

from . import (
    base,
    event_logger,
)

api_router: APIRouter = APIRouter()
api_router.include_router(base.router)
api_router.include_router(event_logger.router)
