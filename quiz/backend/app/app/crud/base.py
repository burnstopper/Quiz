from typing import Generic, Type, TypeVar

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.quiz import CRUDQuiz
from app.crud.template import CRUDTemplate
from app.database.base_class import Base
from app.models.quiz import Quiz
from app.models.template import Template

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


async def check_is_name_unique(crud: CRUDQuiz | CRUDTemplate, item_name: str, db: AsyncSession) -> bool:
    item: Quiz | Template | None = await crud.select_by_name(item_name=item_name.strip(), db=db)
    if item is not None:
        return False
    return True


async def check_conflicts_with_other_names(crud: CRUDQuiz | CRUDTemplate, item_id: int, item_name: str,
                                           db: AsyncSession) -> bool:
    item: Quiz | Template | None = await crud.select_by_name(item_name=item_name.strip(), db=db)
    if item is None or item.id == item_id:
        return True
    return False


async def check_item_id_is_valid(crud: CRUDQuiz | CRUDTemplate, item_id: int, db: AsyncSession) -> bool:
    max_id: int = await crud.get_last_id(db=db)
    return item_id <= max_id
