import uuid
from datetime import datetime

from src.common.schemas import BaseSchema


class AuthUser(BaseSchema):
    username: str
    password: str


class TokenPair(BaseSchema):
    access_token: str
    refresh_token: str


class RefreshToken(BaseSchema):
    refresh_token: str


class JWTPayload(BaseSchema):
    sub: str
    jti: uuid.UUID
    iat: datetime
    exp: datetime
    token_type: str | None
