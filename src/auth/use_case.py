from src.auth import service, jwt
from src.auth.exceptions import InvalidToken
from src.auth.schemas import AuthUser
from src.common.use_case import BaseAsyncUseCase


class CreateTokenPair(BaseAsyncUseCase):
    async def __call__(self, user_in: AuthUser):
        user = await service.authenticate_user(self.session, user_in)
        access_token = service.create_token(token_class=jwt.AccessToken, user=user)
        refresh_token = service.create_token(token_class=jwt.RefreshToken, user=user)
        return {"access_token": access_token, "refresh_token": refresh_token}


class RefreshTokenPair(BaseAsyncUseCase):
    async def __call__(self, token: jwt.RefreshToken):
        user = await service.get_user_from_token(self.session, token)
        await service.add_to_blacklist(self.session, token)
        await self.session.commit()

        access_token = service.create_token(
            token_class=jwt.AccessToken, user=user
        )
        refresh_token = service.create_token(
            token_class=jwt.RefreshToken, user=user
        )

        return {"access_token": access_token, "refresh_token": refresh_token}


class UserLogout(BaseAsyncUseCase):
    async def __call__(self, refresh_token: str):
        token = jwt.RefreshToken(token=refresh_token)
        if await service.in_blacklist(self.session, token):
            raise InvalidToken()

        await service.add_to_blacklist(self.session, token)
        await self.session.commit()
