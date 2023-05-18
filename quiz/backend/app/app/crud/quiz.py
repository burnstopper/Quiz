from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.base import CRUDBase
from app.models.quiz import Quiz
from app.schemas.quiz import QuizCreate, QuizUpdate


class CRUDQuiz(CRUDBase[Quiz]):
    async def create_new_quiz(self, quiz_in: QuizCreate, new_id: int, db: AsyncSession) -> Quiz:
        new_quiz = Quiz(name=quiz_in.name.strip(),
                        template_id=quiz_in.template_id,
                        description=quiz_in.description,
                        invite_link=f'http://{settings.HOST}:{settings.PORT}/invite/quizzes/{new_id}/add'
                        )
        db.add(new_quiz)
        await db.commit()

        return new_quiz

    async def update_quiz(self, quiz_id: int, quiz_in: QuizUpdate, db: AsyncSession) -> Quiz:
        query = (
            update(self.model)
            .where(self.model.id == quiz_id)
            .values(quiz_in.dict(exclude_unset=True))
            .returning(Quiz)
        )

        updated_quiz: Quiz = (await db.execute(query)).scalar()
        await db.commit()

        return updated_quiz

    async def get_all_quizzes(self, db: AsyncSession) -> list[Quiz]:
        query = (
            select(self.model)
        )

        return list((await db.execute(query)).scalars().all())

    async def get_respondent_quizzes(self, quizzes_ids: list[int], db: AsyncSession) -> list[Quiz]:
        query = (
            select(self.model)
            .where(self.model.id.in_(quizzes_ids))
        )

        return list((await db.execute(query)).scalars().all())

    async def get_quiz_by_id(self, quiz_id: int, db: AsyncSession) -> Quiz:
        query = (
            select(self.model)
            .where(self.model.id == quiz_id)
        )

        return (await db.execute(query)).scalar()

    async def get_quizzes_by_template_id(self, template_id: int, db: AsyncSession) -> list[Quiz]:
        query = (
            select(self.model)
            .where(self.model.template_id == template_id)
        )

        return list((await db.execute(query)).scalars().all())


crud = CRUDQuiz(Quiz)
