from typing import Generic, Type, TypeVar

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


# Base class for Quiz and Template models
class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def select_by_name(self, item_name: str, db: AsyncSession) -> ModelType:
        query = (
            select(self.model)
            .where(self.model.name == item_name)
        )
        item = (await db.execute(query)).scalar()

        return item

    async def get_last_id(self, db: AsyncSession) -> int:
        query = (
            func.max(self.model.id)
        )

        max_id: int = (await db.execute(query)).scalar()
        if max_id is None:
            return 0
        return max_id
