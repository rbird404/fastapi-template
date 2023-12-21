from pydantic import BaseModel
from typing import Optional, Any


class BaseSchema(BaseModel):
    pass


class DefaultResponse(BaseSchema):
    status: bool
    msg: str
    details: Optional[dict[Any, Any]] = {}
