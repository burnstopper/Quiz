from typing import Type, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.quiz import Quiz
from app.models.template import Template
from app.models.quiz_respondent import QuizRespondent


async def check_is_name_unique(model: Type[Quiz | Template], item_name: str, db: AsyncSession) -> bool:
    query = (
        select(model.name)
        .where(model.name == item_name.strip())
    )

    is_used_name: str | None = (await db.execute(query)).first()
    if is_used_name is not None:
        return False
    return True


async def check_conflicts_with_other_names(model: Type[Quiz | Template], item_id: int, item_name: str,
                                           db: AsyncSession) -> bool:
    query = (
        select(model.id)
        .where(model.name == item_name.strip())
    )

    result_id: int = (await db.execute(query)).scalar()
    if result_id is None:
        return True
    elif result_id != item_id:
        return False
    return True


async def get_max_id(model: Type[Quiz | Template], db: AsyncSession) -> int:
    query = (
        func.max(model.id)
    )

    max_id: int = (await db.execute(query)).scalar()
    if max_id is None:
        return 0
    return max_id


async def check_id_is_valid(model: Type[Quiz | Template], item_id: int, db: AsyncSession) -> bool:
    max_id: int = await get_max_id(model, db=db)
    return item_id <= max_id


async def has_respondent_added_to_quiz(quiz_id: int, respondent_id: int, db: AsyncSession) -> bool:
    query = (
        select(QuizRespondent)
        .where(
            (QuizRespondent.quiz_id == quiz_id) & (QuizRespondent.respondent_id == respondent_id)
        )
    )

    quiz_respondent: QuizRespondent = (await db.execute(query)).scalar()
    if quiz_respondent is None:
        return False
    return True
