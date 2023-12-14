from src.database import AsyncDbSession
from src.auth import service
from src.users.exceptions import UsernameTaken
from src.users.schemas import UserCreate


async def valid_user_create(session: AsyncDbSession, user_in: UserCreate) -> UserCreate:
    if await service.get_user_by_username(session, user_in.username):
        raise UsernameTaken()

    return user_in
