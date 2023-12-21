from src.auth.service import CurrentUser
from src.common.use_case import BaseAsyncUseCase, BaseUseCase
from src.users import service
from src.users.exceptions import UsernameTaken
from src.users.schemas import UserCreate, UserResponse


class CreateUser(BaseAsyncUseCase):
    async def __call__(self, user_in: UserCreate) -> UserResponse:
        if await service.get_user_by_username(self.session, user_in.username):
            raise UsernameTaken()

        user = await service.create_user(self.session, user_in)
        await self.session.commit()
        return UserResponse(msg="Registration was successful.", details=user)


class GetCurrentUser(BaseUseCase):
    def __init__(self, current_user: CurrentUser):
        self.user = current_user

    def __call__(self, *args, **kwargs) -> UserResponse:
        return UserResponse(msg="Current user successfully obtained.", details=self.user)
