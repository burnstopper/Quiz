import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings
from app.database.base import *

# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
# turn on 'echo=True' only for testing purposes
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_models() -> None:
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_models())
