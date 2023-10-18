from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.jwt import bearer_token
from src.database import AsyncDbSession
from src.auth import service, tokens
from src.auth.exceptions import RefreshTokenNotValid, UsernameTaken, AccessTokenNotValid
from src.auth.schemas import RefreshToken, UserCreate


async def valid_refresh_token(session: AsyncDbSession, token: RefreshToken) -> tokens.RefreshToken:
    token = tokens.RefreshToken(token=token.refresh_token)

    if not await token.in_whitelist(session):
        raise RefreshTokenNotValid()

    return token


async def valid_access_token(
        session: AsyncDbSession, token: HTTPAuthorizationCredentials = Depends(bearer_token)
) -> tokens.AccessToken:
    token = tokens.AccessToken(token=token.credentials)

    if not await token.in_whitelist(session):
        raise AccessTokenNotValid()

    return token


async def valid_user_create(session: AsyncDbSession, user_in: UserCreate) -> UserCreate:
    if await service.get_user_by_username(session, user_in.username):
        raise UsernameTaken()

    return user_in
