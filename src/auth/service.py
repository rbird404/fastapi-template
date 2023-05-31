import uuid
from datetime import datetime, timedelta

from pydantic.types import UUID4
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.config import auth_config
from src.auth.exceptions import InvalidCredentials
from src.auth.schemas import AuthUser
from src.auth.security import check_password, hash_password
from src.auth.models import User, Token
from src.database import session
from src import utils


@session
async def create_user(user: AuthUser, *, session: AsyncSession) -> User | None:
    new_user = User(**user.dict())
    new_user.password = hash_password(user.password)
    session.add(new_user)
    return new_user


@session
async def get_user_by_id(user_id: int, *, session: AsyncSession) -> User | None:
    user = await session.scalar(
        select(User).where(User.id == user_id)
    )
    return user


@session
async def get_user_by_email(email: str, *, session: AsyncSession) -> User | None:
    user = await session.scalar(
        select(User).where(User.email == email)
    )
    return user


@session
async def create_refresh_token(
        *, user_id: int, refresh_token: str | None = None, session: AsyncSession
) -> str:
    if not refresh_token:
        refresh_token = utils.generate_random_alphanum(64)

        token = Token(
            uuid=uuid.uuid4(),
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
            user_id=user_id
        )
        session.add(token)

    return refresh_token


@session
async def get_refresh_token(refresh_token: str, *, session: AsyncSession) -> Token | None:
    token = await session.scalar(
        select(Token).where(Token.refresh_token == refresh_token)
    )
    return token


@session
async def expire_refresh_token(refresh_token_uuid: UUID4, *, session: AsyncSession) -> None:
    await session.execute(
        update(Token)
        .values(expires_at=datetime.utcnow() - timedelta(days=1))
        .where(Token.uuid == refresh_token_uuid)
    )


async def authenticate_user(auth_data: OAuth2PasswordRequestForm) -> User:
    user = await get_user_by_email(auth_data.username)
    if not user:
        raise InvalidCredentials()

    if not check_password(auth_data.password, user.password):
        raise InvalidCredentials()

    return user
