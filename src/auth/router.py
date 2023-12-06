from fastapi import APIRouter, Depends

from src.auth import service, jwt
from src.auth import validators
from src.auth.exceptions import InvalidToken
from src.auth.schemas import TokenPair, AuthUser, RefreshToken
from src.database import AsyncDbSession

router = APIRouter()


@router.post("/token", response_model=TokenPair)
async def token_obtain_pair(
        session: AsyncDbSession,
        auth_data: AuthUser
):
    user = await service.authenticate_user(session, auth_data)
    access_token = service.create_token(token_class=jwt.AccessToken, user=user)
    refresh_token = service.create_token(token_class=jwt.RefreshToken, user=user)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/token/refresh", response_model=TokenPair)
async def refresh_tokens(
        session: AsyncDbSession,
        token: jwt.RefreshToken = Depends(validators.valid_refresh_token)
):
    user = await service.get_user_from_token(session, token)
    await service.add_to_blacklist(session, token)
    await session.commit()

    access_token = service.create_token(
        token_class=jwt.AccessToken, user=user
    )
    refresh_token = service.create_token(
        token_class=jwt.RefreshToken, user=user
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/token/logout")
async def logout(
        session: AsyncDbSession,
        refresh_token: RefreshToken,
):
    refresh_token = jwt.RefreshToken(token=refresh_token.refresh_token)
    if await service.in_blacklist(session, refresh_token):
        raise InvalidToken()

    await service.add_to_blacklist(session, refresh_token)
    await session.commit()
