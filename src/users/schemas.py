from pydantic import Field, ConfigDict
from src.common.schemas import BaseSchema


class UserBase(BaseSchema):
    model_config = ConfigDict(from_attributes=True)
    username: str


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=128)


class UserRead(UserBase):
    id: int
