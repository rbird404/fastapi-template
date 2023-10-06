from typing import Annotated
from fastapi import Depends

from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine, AsyncSession
)

from src.config import settings

__all__ = ("Base", "DATABASE_URL", "AsyncDbSession")

DATABASE_URL = str(settings.DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
        finally:
            await session.close()


AsyncDbSession = Annotated[AsyncSession, Depends(get_async_session)]


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
