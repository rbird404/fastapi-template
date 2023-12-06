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

    access_token = await service.create_token(
        session, token_class=jwt.AccessToken, user=user
    )
    refresh_token = await service.create_token(
        session, token_class=jwt.RefreshToken, user=user
    )
    await session.commit()
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/token/refresh", response_model=TokenPair)
async def refresh_tokens(
        session: AsyncDbSession,
        token: jwt.RefreshToken = Depends(validators.valid_refresh_token)
):
    user = await service.get_user_from_token(session, token)
    await service.remove_from_whitelist(session, token)

    access_token = await service.create_token(
        session, token_class=jwt.AccessToken, user=user
    )
    refresh_token = await service.create_token(
        session, token_class=jwt.RefreshToken, user=user
    )
    await session.commit()
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/token/logout")
async def logout(
        session: AsyncDbSession,
        refresh_token: RefreshToken,
        access_token: jwt.AccessToken = Depends(validators.valid_access_token),
):
    refresh_token = jwt.RefreshToken(token=refresh_token.refresh_token)
    if not await service.in_whitelist(session, refresh_token):
        raise InvalidToken()

    if refresh_token["sub"] != access_token["sub"]:
        raise InvalidToken()

    await service.remove_from_whitelist(session, refresh_token)
    await service.remove_from_whitelist(session, access_token)
    await session.commit()
