import uuid
from jose import jwt, JWTError
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer

from src.auth.config import auth_config
from src.auth.exceptions import InvalidToken
from src.models import ORJSONModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)


def encode(payload: dict) -> str:
    return jwt.encode(payload, auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG)


def decode(token: str, verify=True) -> dict:
    if verify:
        try:
            return jwt.decode(token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG])
        except JWTError:
            raise InvalidToken()

    return jwt.get_unverified_claims(token)


class JWTPayload(ORJSONModel):
    sub: str
    jti: uuid.UUID
    iat: datetime
    exp: datetime
    token_type: str | None
