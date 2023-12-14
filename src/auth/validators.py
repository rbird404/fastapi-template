from src.auth.service import in_blacklist
from src.database import AsyncDbSession
from src.auth import jwt
from src.auth.exceptions import RefreshTokenNotValid
from src.auth.schemas import RefreshToken


async def valid_refresh_token(session: AsyncDbSession, token: RefreshToken) -> jwt.RefreshToken:
    token = jwt.RefreshToken(token=token.refresh_token)

    if await in_blacklist(session, token):
        raise RefreshTokenNotValid()

    return token
