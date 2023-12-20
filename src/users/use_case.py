from src.common.use_case import BaseAsyncUseCase
from src.users import service
from src.users.exceptions import UsernameTaken
from src.users.models import User
from src.users.schemas import UserCreate


class CreateUser(BaseAsyncUseCase):
    async def __call__(self, user_in: UserCreate) -> User:
        if await service.get_user_by_username(self.session, user_in.username):
            raise UsernameTaken()

        user = await service.create_user(self.session, user_in)
        await self.session.commit()
        return user
