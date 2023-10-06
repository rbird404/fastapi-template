from typing import Annotated

from pydantic import BeforeValidator
import datetime


def convert_datetime(datetime_: datetime.datetime):
    return datetime_.strftime("%d.%m.%Y %H:%M")


DateTimeField = Annotated[str, BeforeValidator(convert_datetime)]
