from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.checkers import check_id_is_valid
from app.api.get_tests import get_tests
from app.crud.quiz import crud as crud_quizzes
from app.database.dependencies import get_db
from app.schemas.quiz_results import QuizResults
from app.schemas.template_test import TemplateTest

router = APIRouter()


async def get_quiz_results(quiz_id: int, db: AsyncSession) -> QuizResults:
    is_valid: bool = await check_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz with this id does not exist')

    quiz_template_id: int = (await crud_quizzes.get_quiz_by_id(quiz_id=quiz_id, db=db)).template_id
    tests: list[TemplateTest] = await get_tests(template_id=quiz_template_id, db=db)
    results: list[list[dict[str, int]] | None] = [None] * len(tests)
    # Добавить обращение к команде тестов

    return QuizResults(**{'quiz_id': quiz_id, 'results': results})


@router.get('/')
async def get_quizzes_results(quizzes_ids: Annotated[list[int], Query()],
                              db: AsyncSession = Depends(get_db)) -> list[QuizResults]:
    results: list[QuizResults | None] = [None] * len(quizzes_ids)
    for i in range(len(quizzes_ids)):
        results[i] = await get_quiz_results(quiz_id=quizzes_ids[i], db=db)

    return results
