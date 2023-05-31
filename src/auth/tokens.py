import uuid
from datetime import datetime, timedelta
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.auth.config import auth_config
from src.auth.exceptions import InvalidToken
from src.auth.jwt import JWTPayload
from src.auth.models import WhitelistedToken, User
from src.auth import jwt


class Token:
    lifetime: timedelta | None = None
    token_type: str | None = None

    def __init__(self, token: str | None = None, verify: bool = True):
        self.token = token
        self.current_time = datetime.utcnow()

        if token is not None:
            self.payload = jwt.decode(token, verify)
            self.verify()
        else:
            self.payload = {"token_type": self.token_type}
            self._set_iat()
            self._set_exp()
            self._set_jti()

    def __repr__(self) -> str:
        return repr(self.payload)

    def __str__(self):
        return jwt.encode(self.payload)

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

    async def in_whitelist(self, session: AsyncSession) -> bool:
        token = await session.scalar(
            select(WhitelistedToken).where(
                WhitelistedToken.jti == self.payload["jti"]  # type:ignore
            )
        )
        return bool(token)

    async def add_to_whitelist(self, session: AsyncSession) -> WhitelistedToken:
        token = WhitelistedToken(
            jti=self.payload['jti'],
            user_id=int(self.payload['sub']),
            expires_at=self.payload['exp'],
        )
        session.add(token)
        await session.commit()
        return token

    async def remove_from_whitelist(self, session: AsyncSession) -> None:
        await session.execute(
            delete(WhitelistedToken).where(
                WhitelistedToken.jti == self.payload['jti']  # type:ignore
            )
        )
        await session.commit()


class AccessToken(Token):
    lifetime = timedelta(minutes=auth_config.JWT_EXP)
    token_type = "access"


class RefreshToken(Token):
    lifetime = timedelta(seconds=auth_config.REFRESH_TOKEN_EXP)
    token_type = "refresh"
