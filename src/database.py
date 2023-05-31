from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, DeclarativeBase
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine
)
from functools import wraps

from src.config import settings

__all__ = ("session", "Base", "DATABASE_URL")

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


def session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                return await func(*args, **kwargs, session=session)
            finally:
                await session.commit()
    return wrapper


class Base(DeclarativeBase):
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime, server_onupdate=func.now())
