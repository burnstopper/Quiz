from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quiz_respondent import QuizRespondent


class CRUDQuizRespondent:
    def __init__(self, model: Type[QuizRespondent]):
        self.model = model

    async def has_respondent_added_to_quiz(self, db: AsyncSession, quiz_id: int, respondent_id: int) -> bool:
        query = (
            select(self.model)
            .where(
                (self.model.quiz_id == quiz_id) & (self.model.respondent_id == respondent_id)
            )
        )

        has_respondent_added_to_quiz: QuizRespondent = (await db.execute(query)).scalar()

        if has_respondent_added_to_quiz is None:
            return False
        return True

    async def add_respondent(self, db: AsyncSession, quiz_id: int, respondent_id: int):

        has_added: bool = await self.has_respondent_added_to_quiz(db=db, quiz_id=quiz_id, respondent_id=respondent_id)

        if has_added:
            return f'Respondent has already added to this quiz'

        new_quiz_respondent = QuizRespondent(respondent_id=respondent_id, quiz_id=quiz_id)
        db.add(new_quiz_respondent)
        await db.commit()

    async def check_access_to_quizz(self, db: AsyncSession, quiz_id: int, respondent_id: int) -> bool:
        has_added: bool = await self.has_respondent_added_to_quiz(quiz_id=quiz_id, respondent_id=respondent_id)
        if has_added:
            return True
        else:
            return False


crud = CRUDQuizRespondent(QuizRespondent)
