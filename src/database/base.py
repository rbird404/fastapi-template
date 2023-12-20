from typing import Type
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    ...


async def remove_by_id(session: AsyncSession, model: Type[Base], id_: int) -> Base:
    obj = await session.scalar(
        delete(model).where(model.id == id_).returning(model)
    )
    return obj
