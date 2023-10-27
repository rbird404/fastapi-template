from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine
)

from src.config import settings


DATABASE_URL = str(settings.DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    echo=False
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

