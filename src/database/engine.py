from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

DATABASE_URL = str(settings.DATABASE_URL)

async_engine = create_async_engine(DATABASE_URL, echo=False)

sync_engine = create_engine(DATABASE_URL, echo=False)

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
