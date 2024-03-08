import os
import pytest
import pytest_asyncio
from alembic.command import upgrade, downgrade
from sqlalchemy import create_engine

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient

from testcontainers.postgres import PostgresContainer
from alembic.config import Config as AlembicConfig
from src.config import Config
from src.database.dependency import get_async_session
from tests.factories.base import BaseFactory


@pytest.fixture(scope="session")
def init_postgres() -> PostgresContainer:
    with PostgresContainer() as postgres:
        os.environ["POSTGRES_HOST"] = postgres.get_container_host_ip()
        os.environ["POSTGRES_PORT"] = postgres.get_exposed_port(5432)
        os.environ["POSTGRES_DB"] = postgres.POSTGRES_DB
        os.environ["POSTGRES_USER"] = postgres.POSTGRES_USER
        os.environ["POSTGRES_PASSWORD"] = postgres.POSTGRES_PASSWORD
        yield postgres


@pytest.fixture(scope="session")
def settings(init_postgres: PostgresContainer):
    return Config()


@pytest.fixture
def migrations(settings) -> None:
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.get_db_url())
    upgrade(alembic_cfg, "head")
    yield
    downgrade(alembic_cfg, "base")


@pytest_asyncio.fixture
async def db_session(migrations, settings) -> AsyncSession:
    async_engine = create_async_engine(
        settings.get_db_url(async_=True), echo=False
    )

    async_session = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        autoflush=False,
    )
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
        finally:
            await session.close()


@pytest.fixture
def db_sync_session(migrations, settings) -> AsyncSession:
    sync_engine = create_engine(
        settings.get_db_url(async_=False), echo=False
    )

    sync_session = sessionmaker(
        bind=sync_engine,
        expire_on_commit=False,
        autoflush=False,
    )

    with sync_session() as session:
        try:
            yield session
        except Exception:
            session.rollback()
        finally:
            session.close()


@pytest.fixture(autouse=True)
def set_factory_session(db_sync_session: Session) -> None:
    BaseFactory.set_session(db_sync_session)


@pytest.fixture(scope="session")
def client(settings) -> TestClient:
    from src.main import app

    async def test_session():
        async_engine = create_async_engine(settings.get_db_url(async_=True), echo=False)

        async_session = async_sessionmaker(
            bind=async_engine,
            expire_on_commit=False,
            autoflush=False,
        )
        async with async_session() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
            finally:
                await session.close()

    app.dependency_overrides[get_async_session] = test_session

    with TestClient(app) as client:
        yield client
