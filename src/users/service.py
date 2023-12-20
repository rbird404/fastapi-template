from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.schemas import UserCreate
from src.users.models import User


async def create_user(session: AsyncSession, user_in: UserCreate, ) -> User | None:
    user = User(**user_in.model_dump(exclude={"password"}))
    user.set_password(user_in.password)
    session.add(user)
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    user = await session.scalar(
        select(User).where(User.id == user_id)
    )
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    user = await session.scalar(
        select(User).where(User.username == username)
    )
    return user
