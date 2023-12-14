import uuid
from datetime import datetime

from pydantic import BaseModel


class AuthUser(BaseModel):
    username: str
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class JWTPayload(BaseModel):
    sub: str
    jti: uuid.UUID
    iat: datetime
    exp: datetime
    token_type: str | None
