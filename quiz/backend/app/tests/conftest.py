import asyncio
from typing import AsyncGenerator
from typing import AsyncIterator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.database.base import *

TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///tests/test_storage/test_quizzes_database.db"
settings.SQLALCHEMY_DATABASE_URL = TEST_SQLALCHEMY_DATABASE_URL

from app.database.dependencies import get_db
from app.main import app

# DATABASE
engine_test = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(bind=engine_test, expire_on_commit=False, class_=AsyncSession)


async def override_get_db() -> AsyncIterator[sessionmaker]:
    async with async_session_maker() as session:
        async with session.begin():
            yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
