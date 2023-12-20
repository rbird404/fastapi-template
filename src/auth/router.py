from fastapi import APIRouter

from src.auth import jwt
from src.auth.schemas import TokenPair, AuthUser, RefreshToken
from src.auth.use_case import CreateTokenPair, UserLogout, RefreshTokenPair

router = APIRouter()


@router.post("/token", response_model=TokenPair)
async def token_obtain_pair(
        auth_data: AuthUser, use_case: CreateTokenPair,
):
    return await use_case(auth_data)


@router.post("/token/refresh", response_model=TokenPair)
async def refresh_tokens(
        use_case: RefreshTokenPair, token: jwt.RefreshToken
):
    return await use_case(token)


@router.post("/token/logout")
async def logout(
        use_case: UserLogout, refresh_token: RefreshToken,
):
    return await use_case(refresh_token.refresh_token)
