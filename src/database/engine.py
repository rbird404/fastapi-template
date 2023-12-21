from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

async_engine = create_async_engine(settings.get_db_url(), echo=False)

sync_engine = create_engine(settings.get_db_url(async_=False), echo=False)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
)

sync_session = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
    autoflush=False,
)
