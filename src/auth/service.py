from typing import Annotated, Type

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import InvalidCredentials, AuthorizationFailed, InvalidToken
from src.auth.jwt import bearer_token
from src.auth.schemas import UserCreate, AuthUser
from src.auth.security import check_password, hash_password
from src.auth.models import User
from src.auth.tokens import Token, AccessToken
from src.database import AsyncDbSession


async def create_user(session: AsyncSession, user_in: UserCreate, ) -> User | None:
    user = User(**user_in.model_dump())
    user.password = hash_password(user_in.password)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    user = await session.scalar(
        select(User).where(User.id == user_id)
    )
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    user = await session.scalar(
        select(User).where(User.username == username)
    )
    return user


async def create_token(
        session: AsyncSession, token_class: Type[Token], user: User
) -> str:
    token = token_class.for_user(user)
    await token.add_to_whitelist(session)
    return str(token)


async def get_user_from_token(session: AsyncSession, token: Token) -> User:
    try:
        user = await get_user_by_id(session, int(token['sub']))
    except (KeyError, ValueError):
        raise InvalidToken()

    if not user:
        raise AuthorizationFailed()

    return user


async def authenticate_user(session: AsyncSession, auth_data: AuthUser) -> User:
    user = await get_user_by_username(session, auth_data.username)
    if not user:
        raise InvalidCredentials()

    if not check_password(auth_data.password, user.password):
        raise InvalidCredentials()

    return user


async def get_current_user(
        session: AsyncDbSession, token: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> User:
    token = AccessToken(token=token.credentials)
    if not await token.in_whitelist(session):
        raise InvalidToken()

    return await get_user_from_token(session, token)


CurrentUser = Annotated[User, Depends(get_current_user)]
