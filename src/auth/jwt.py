import uuid
from datetime import datetime, timedelta

from jose import jwt, JWTError
from pydantic import ValidationError
from fastapi.security import HTTPBearer

from src.auth.config import auth_config
from src.auth.exceptions import InvalidToken
from src.auth.schemas import JWTPayload
from src.users.models import User

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


class Token:
    lifetime: timedelta | None = None
    token_type: str | None = None

    def __init__(self, token: str | None = None, verify: bool = True):
        self.token = token
        self.current_time = datetime.utcnow()

        if token is not None:
            self.payload = decode(token, verify)
            self.verify()
        else:
            self.payload = {"token_type": self.token_type}
            self._set_iat()
            self._set_exp()
            self._set_jti()

    def __repr__(self) -> str:
        return repr(self.payload)

    def __str__(self):
        return encode(self.payload)

    def __getitem__(self, item: str):
        return self.payload[item]

    def __setitem__(self, key, value):
        self.payload[key] = value

    def _set_jti(self):
        self.payload["jti"] = uuid.uuid4().hex

    def _set_iat(self):
        self.payload["iat"] = self.current_time

    def _set_exp(self):
        self.payload["exp"] = self.current_time + self.lifetime

    def verify(self):
        try:
            JWTPayload(**self.payload)
        except ValidationError:
            raise InvalidToken()

        if self.payload.get("token_type") != self.token_type:
            raise InvalidToken()

    @classmethod
    def for_user(cls, user: User) -> "Token":
        token = cls()
        token["sub"] = str(user.id)
        return token


class AccessToken(Token):
    lifetime = timedelta(minutes=auth_config.JWT_EXP)
    token_type = "access"


class RefreshToken(Token):
    lifetime = timedelta(seconds=auth_config.REFRESH_TOKEN_EXP)
    token_type = "refresh"
