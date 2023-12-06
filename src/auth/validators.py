from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.service import in_whitelist
from src.database import AsyncDbSession
from src.auth import jwt
from src.auth.exceptions import RefreshTokenNotValid, AccessTokenNotValid
from src.auth.schemas import RefreshToken


async def valid_refresh_token(session: AsyncDbSession, token: RefreshToken) -> jwt.RefreshToken:
    token = jwt.RefreshToken(token=token.refresh_token)

    if not await in_whitelist(session, token):
        raise RefreshTokenNotValid()

    return token


async def valid_access_token(
        session: AsyncDbSession, token: HTTPAuthorizationCredentials = Depends(jwt.bearer_token)
) -> jwt.AccessToken:
    token = jwt.AccessToken(token=token.credentials)

    if not await in_whitelist(session, token):
        raise AccessTokenNotValid()

    return token
