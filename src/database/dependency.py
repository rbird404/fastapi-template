from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.engine import async_session


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
        finally:
            await session.close()


AsyncDbSession = Annotated[AsyncSession, Depends(get_async_session)]
