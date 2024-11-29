from typing_extensions import TypedDict
import datetime


class TestResponse(TypedDict):
    now: datetime.datetime
