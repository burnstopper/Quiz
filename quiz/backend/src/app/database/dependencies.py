from typing import AsyncIterator

from sqlalchemy.orm import sessionmaker

from app.database.session import AsyncSessionLocal


# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#a-database-dependency-with-yield
async def get_db() -> AsyncIterator[sessionmaker]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session
