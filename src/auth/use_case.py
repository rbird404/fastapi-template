from src.auth import service, jwt
from src.auth.exceptions import InvalidToken
from src.auth.schemas import AuthUser, TokenResponse
from src.common.schemas import DefaultResponse
from src.common.use_case import BaseAsyncUseCase


class CreateTokenPair(BaseAsyncUseCase):
    async def __call__(self, user_in: AuthUser) -> TokenResponse:
        user = await service.authenticate_user(self.session, user_in)
        access_token = service.create_token(token_class=jwt.AccessToken, user=user)
        refresh_token = service.create_token(token_class=jwt.RefreshToken, user=user)
        details = {"access_token": access_token, "refresh_token": refresh_token}
        return TokenResponse(msg="Authorization was successful.", details=details)


class RefreshTokenPair(BaseAsyncUseCase):
    async def __call__(self, refresh_token: str) -> TokenResponse:
        token = jwt.RefreshToken(refresh_token)
        user = await service.get_user_from_token(self.session, token)

        if await service.in_blacklist(self.session, token):
            raise InvalidToken()

        await service.add_to_blacklist(self.session, token)
        await self.session.commit()

        access_token = service.create_token(
            token_class=jwt.AccessToken, user=user
        )
        refresh_token = service.create_token(
            token_class=jwt.RefreshToken, user=user
        )

        details = {"access_token": access_token, "refresh_token": refresh_token}
        return TokenResponse(msg="Tokens updated successfully.", details=details)


class UserLogout(BaseAsyncUseCase):
    async def __call__(self, refresh_token: str) -> DefaultResponse:
        token = jwt.RefreshToken(token=refresh_token)
        if await service.in_blacklist(self.session, token):
            raise InvalidToken()

        await service.add_to_blacklist(self.session, token)
        await self.session.commit()
        return DefaultResponse(status=True, msg="User logged out successfully.")
