from pydantic import Field, ConfigDict
from pydantic import BaseModel


class AuthUser(BaseModel):
    username: str
    password: str = Field(min_length=6, max_length=128)


class UserCreate(AuthUser):
    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class RefreshToken(BaseModel):
    refresh_token: str
