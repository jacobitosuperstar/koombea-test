"""FASTAPI Application
"""
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .router import api_router


def main() -> FastAPI:
    app: FastAPI = FastAPI(
        title="KOOMBEA-TEST",
        default_response_class=ORJSONResponse,
    )
    app.include_router(api_router)
    return app

app: FastAPI = main()

if __name__ == "__main__":
    main()
