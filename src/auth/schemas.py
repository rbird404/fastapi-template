import re
from pydantic import Field, validator

from src.models import ORJSONModel

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


class AuthUser(ORJSONModel):
    username: str
    password: str = Field(min_length=6, max_length=128)

    @validator("password")
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )
        return password


class UserCreate(AuthUser):
    username: str
    password: str


class UserRead(ORJSONModel):
    id: int
    username: str


class TokenPair(ORJSONModel):
    access_token: str
    refresh_token: str


class RefreshToken(ORJSONModel):
    refresh_token: str
