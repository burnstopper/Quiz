from typing import Type

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quiz import Quiz
from app.schemas.quiz import QuizCreate, QuizUpdate


class CRUDQuiz:
    def __init__(self, model: Type[Quiz]):
        self.model = model

    async def is_quiz_name_unique(self, db: AsyncSession, quiz_name: str, quiz_id: int = None) -> bool:
        if quiz_id is None:
            query = (
                select(self.model.name)
                .where(self.model.name == quiz_name.strip())
            )

            has_quiz_name_added: str = (await db.execute(query)).scalar()

            if has_quiz_name_added is None:
                return True
            return False
        else:
            query = (
                select(self.model.id)
                .where(self.model.name == quiz_name.strip())
            )

            result_quiz_id: int = (await db.execute(query)).scalar()

            if result_quiz_id != quiz_id:
                return False
            return True

    async def create_new_quiz(self, db: AsyncSession, quiz_in: QuizCreate) -> str | None:
        is_unique_: bool = await self.is_quiz_name_unique(db=db, quiz_name=quiz_in.name)

        # quiz with this name has been already created
        if not is_unique_:
            return f'Quiz with this name "{quiz_in.name}" has already been created'

        new_quiz = Quiz(name=quiz_in.name.strip(),
                        template_id=quiz_in.template_id,
                        description=quiz_in.description
                        )
        db.add(new_quiz)
        await db.commit()

    async def update_quiz(self, db: AsyncSession, quiz_id: int, quiz_in: QuizUpdate) -> str | None:
        is_unique: bool = await self.is_quiz_name_unique(db=db, quiz_name=quiz_in.name, quiz_id=quiz_id)

        # quiz with this name has been already created
        if not is_unique:
            return f'Quiz with this name "{quiz_in.name}" has already been created'

        query = (
            update(self.model)
            .where(self.model.id == quiz_id)
            .values(quiz_in.dict(exclude_unset=True))
            .returning(Quiz)
        )

        await db.execute(query)

        await db.commit()

    async def get_all_quizzes(self, db: AsyncSession) -> list[Quiz]:
        query = (
            select(self.model)
        )

        return list((await db.execute(query)).scalars().all())

    async def get_respondent_quizzes(self, db: AsyncSession, quizzes_ids: list[int]) -> list[Quiz]:
        query = (
            select(self.model)
            .where(self.model.id.in_(quizzes_ids))
        )

        return list((await db.execute(query)).scalars().all())

    async def get_quiz_by_id(self, db: AsyncSession, quiz_id: int) -> (Quiz | None, str | None):
        query = (
            select(self.model)
            .where(self.model.id == quiz_id)
        )

        quiz = (await db.execute(query)).scalar()
        if quiz is not None:
            return quiz, None
        return None, f'Quiz with this id {quiz_id} does not exist'


crud = CRUDQuiz(Quiz)
