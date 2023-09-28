import re
from pydantic import Field, field_validator

from src.schemas import BaseSchema

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


class AuthUser(BaseSchema):
    username: str
    password: str = Field(min_length=6, max_length=128)

    @field_validator("password", mode="after")
    @classmethod
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


class UserRead(BaseSchema):
    id: int
    username: str


class TokenPair(BaseSchema):
    access_token: str
    refresh_token: str


class RefreshToken(BaseSchema):
    refresh_token: str
