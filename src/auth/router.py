from fastapi import APIRouter, Depends, status

from src.auth import service, tokens
from src.auth import validators
from src.auth.exceptions import InvalidToken
from src.auth.schemas import UserRead, UserCreate, TokenPair, AuthUser, RefreshToken
from src.auth.service import CurrentUser
from src.database import AsyncDbSession

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register_user(
        session: AsyncDbSession,
        user_in: UserCreate = Depends(validators.valid_user_create),
):
    user = await service.create_user(session, user_in)
    await session.commit()
    return user


@router.get("/users/me", response_model=UserRead)
async def get_me(current_user: CurrentUser):
    return current_user


@router.post("/token", response_model=TokenPair)
async def token_obtain_pair(
        session: AsyncDbSession,
        auth_data: AuthUser
):
    user = await service.authenticate_user(session, auth_data)

    access_token = await service.create_token(
        session, token_class=tokens.AccessToken, user=user
    )
    refresh_token = await service.create_token(
        session, token_class=tokens.RefreshToken, user=user
    )
    await session.commit()
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/token/refresh", response_model=TokenPair)
async def refresh_tokens(
        session: AsyncDbSession,
        token: tokens.RefreshToken = Depends(validators.valid_refresh_token)
):
    user = await service.get_user_from_token(session, token)
    await token.remove_from_whitelist(session)

    access_token = await service.create_token(
        session, token_class=tokens.AccessToken, user=user
    )
    refresh_token = await service.create_token(
        session, token_class=tokens.RefreshToken, user=user
    )
    await session.commit()
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/token/logout")
async def logout(
        session: AsyncDbSession,
        refresh_token: RefreshToken,
        access_token: tokens.AccessToken = Depends(validators.valid_access_token),
):
    refresh_token = tokens.RefreshToken(token=refresh_token.refresh_token)
    if not await refresh_token.in_whitelist(session):
        raise InvalidToken()

    if refresh_token["sub"] != access_token["sub"]:
        raise InvalidToken()

    await refresh_token.remove_from_whitelist(session)
    await access_token.remove_from_whitelist(session)
    await session.commit()
