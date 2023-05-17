from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quiz_respondent import QuizRespondent


class CRUDQuizRespondents:
    def __init__(self, model: Type[QuizRespondent]):
        self.model = model

    async def add_respondent(self, quiz_id: int, respondent_id: int, db: AsyncSession):
        new_quiz_respondent = QuizRespondent(quiz_id=quiz_id, respondent_id=respondent_id)
        db.add(new_quiz_respondent)
        await db.commit()

    async def select_respondent_quiz(self, quiz_id: int, respondent_id: int, db: AsyncSession) -> QuizRespondent:
        query = (
            select(self.model)
            .where(
                (self.model.quiz_id == quiz_id) & (self.model.respondent_id == respondent_id)
            )
        )

        return (await db.execute(query)).scalar()

    async def get_respondent_quizzes(self, respondent_id: int, db: AsyncSession) -> list[int]:
        query = (
            select(self.model.quiz_id)
            .where(self.model.respondent_id == respondent_id)
        )

        return list((await db.execute(query)).scalars().all())

    async def get_quiz_respondents(self, quiz_id: int, db: AsyncSession) -> list[int]:
        query = (
            select(self.model.respondent_id)
            .where(self.model.quiz_id == quiz_id)
        )

        return list((await db.execute(query)).scalars().all())


crud = CRUDQuizRespondents(QuizRespondent)
