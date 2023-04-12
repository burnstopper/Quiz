from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quiz_respondent import QuizRespondent


class CRUDQuizRespondent:
    def __init__(self, model: Type[QuizRespondent]):
        self.model = model

    async def add_respondent(self, quiz_id: int, respondent_id: int, db: AsyncSession):
        new_quiz_respondent = QuizRespondent(quiz_id=quiz_id, respondent_id=respondent_id)
        db.add(new_quiz_respondent)
        await db.commit()

    async def get_respondent_quizzes(self, respondent_id: int, db: AsyncSession) -> list[int]:
        query = (
            select(self.model.quiz_id)
            .where(self.model.respondent_id == respondent_id)
        )

        return list((await db.execute(query)).scalars().all())


crud = CRUDQuizRespondent(QuizRespondent)