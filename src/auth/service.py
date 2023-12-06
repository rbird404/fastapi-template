from datetime import datetime
from typing import Annotated, Type

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import InvalidCredentials, AuthorizationFailed, InvalidToken
from src.auth.models import BlacklistedToken
from src.auth.schemas import AuthUser
from src.users.models import User
from src.auth.jwt import Token, AccessToken, bearer_token
from src.database import AsyncDbSession
from src.users.service import get_user_by_id, get_user_by_username


async def in_blacklist(session: AsyncSession, token: Token) -> bool:
    token_in_db = await session.scalar(
        select(BlacklistedToken).where(
            BlacklistedToken.jti == token["jti"]  # type:ignore
        )
    )
    return bool(token_in_db)


async def add_to_blacklist(session: AsyncSession, token: Token) -> BlacklistedToken:
    token_obj = BlacklistedToken(
        jti=token['jti'],
        user_id=int(token['sub']),
        expires_at=datetime.fromtimestamp(token['exp']),
    )
    session.add(token_obj)
    return token_obj


def create_token(token_class: Type[Token], user: User) -> str:
    token = token_class.for_user(user)
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

    if not user.check_password(auth_data.password):
        raise InvalidCredentials()

    return user


async def get_current_user(
        session: AsyncDbSession, token: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> User:
    token = AccessToken(token=token.credentials)
    if await in_blacklist(session, token):
        raise InvalidToken()

    return await get_user_from_token(session, token)


CurrentUser = Annotated[User, Depends(get_current_user)]
