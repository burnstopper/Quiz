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


async def has_respondent_added_to_quiz(crud_quiz_respondents: CRUDQuizRespondents, quiz_id: int,
                                       respondent_id: int, db: AsyncSession) -> bool:
    quiz_respondent: QuizRespondent = await crud_quiz_respondents.select_respondent_quiz(quiz_id=quiz_id,
                                                                                         respondent_id=respondent_id,
                                                                                         db=db)

    if quiz_respondent is None:
        return False
    return True


crud = CRUDQuizRespondents(QuizRespondent)
