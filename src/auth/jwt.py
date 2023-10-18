import uuid
from jose import jwt, JWTError
from datetime import datetime
from fastapi.security import HTTPBearer

from src.auth.config import auth_config
from src.auth.exceptions import InvalidToken
from pydantic import BaseModel

bearer_token = HTTPBearer()


def encode(payload: dict) -> str:
    return jwt.encode(payload, auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG)


def decode(token: str, verify=True) -> dict:
    if verify:
        try:
            return jwt.decode(token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG])
        except JWTError:
            raise InvalidToken()

    return jwt.get_unverified_claims(token)


class JWTPayload(BaseModel):
    sub: str
    jti: uuid.UUID
    iat: datetime
    exp: datetime
    token_type: str | None
