import asyncio
from typing import Callable
from sqlalchemy import event
from datetime import timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings
from app.database.base import *

# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
# turn on 'echo=True' only for testing purposes
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, echo=False, pool_pre_ping=True,
                             connect_args={'timeout': 10})
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# define scheduler and scheduling function here because of circular import otherwise
async def scheduled_delete_of_expired_requests(crud_delete: Callable, expiration_time: timedelta) -> None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await crud_delete(db=session, expiration_time=expiration_time)


scheduler = AsyncIOScheduler()
# calculate misfire_grace_time (in seconds) on base of the REQUESTS_EXPIRATION_TIME_IN_MINUTES
schedule_params = dict(func=scheduled_delete_of_expired_requests,
                       trigger='interval',
                       minutes=settings.REQUESTS_EXPIRATION_TIME_IN_MINUTES,
                       misfire_grace_time=settings.REQUESTS_EXPIRATION_TIME_IN_MINUTES * 60,
                       coalesce=True,
                       max_instances=1)


# https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
# engine.sync_engine because async events is not yet implemented
# https://github.com/sqlalchemy/sqlalchemy/discussions/6594#discussioncomment-836437
@event.listens_for(engine.sync_engine, "connect")
def do_connect(dbapi_connection, connection_record):
    # disable pysqlite's emitting of the BEGIN statement entirely.
    # also stops it from emitting COMMIT before any DDL.
    dbapi_connection.isolation_level = None

    cursor = dbapi_connection.cursor()
    # https://www.sqlite.org/wal.html
    # Reading and writing can proceed concurrently
    cursor.execute("PRAGMA journal_mode=WAL")
    # https://www.sqlite.org/pragma.html#pragma_synchronous
    cursor.execute('PRAGMA synchronous=NORMAL')
    cursor.close()


# without this decorator rollbacks will not work# it adds second BEGIN and empty raw SQL statements
@event.listens_for(engine.sync_engine, "begin")
def do_begin(conn):
    # emit our own BEGIN
    # IMMEDIATE to let read operations to deal with the most actual information
    conn.exec_driver_sql("BEGIN IMMEDIATE")


async def init_models() -> None:
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_models())
