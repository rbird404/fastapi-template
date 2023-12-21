from fastapi import APIRouter, Depends

from src.auth.schemas import AuthUser, RefreshToken, TokenResponse
from src.auth.use_case import CreateTokenPair, UserLogout, RefreshTokenPair
from src.common.schemas import DefaultResponse

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
async def token_obtain_pair(
        auth_data: AuthUser, use_case: CreateTokenPair = Depends(),
):
    return await use_case(auth_data)


@router.post("/token/refresh", response_model=TokenResponse)
async def refresh_tokens(
        refresh_token: RefreshToken, use_case: RefreshTokenPair = Depends(),
):
    return await use_case(refresh_token.refresh_token)


@router.post("/token/logout", response_model=DefaultResponse)
async def logout(
        refresh_token: RefreshToken, use_case: UserLogout = Depends(),
):
    return await use_case(refresh_token.refresh_token)
