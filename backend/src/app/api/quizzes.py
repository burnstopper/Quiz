from typing import Annotated

from fastapi import APIRouter, Header, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.checkers import check_id_is_valid
from app.api.checkers import check_is_name_unique
from app.crud.quiz import crud as crud_quizzes
from app.crud.quiz_respondents import crud as crud_quiz_respondents
from app.database.dependencies import get_db
from app.models.quiz import Quiz
from app.schemas.quiz import Quiz as RequestedQuiz
from app.schemas.quiz import QuizCreate, QuizUpdate

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=RequestedQuiz)
async def create_quiz(quiz_in: QuizCreate, db: AsyncSession = Depends(get_db)) -> Quiz | None:
    """
    Create new quiz
    """

    is_unique: bool = await check_is_name_unique(model=Quiz, item_name=quiz_in.name, db=db)
    if not is_unique:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Quiz with this name has already been created')

    return await crud_quizzes.create_new_quiz(quiz_in=quiz_in, db=db)


@router.put('/{quiz_id}', status_code=status.HTTP_200_OK, response_model=RequestedQuiz)
async def update_quiz(quiz_id: int, quiz_in: QuizUpdate, db: AsyncSession = Depends(get_db)) -> Quiz | None:
    """
    Update quiz by id
    """

    is_valid: bool = await check_id_is_valid(model=Quiz, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz with this id has does not exist')

    is_unique: bool = await check_is_name_unique(model=Quiz, item_name=quiz_in.name, db=db)
    if not is_unique:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Quiz with this name has already been created')

    return await crud_quizzes.update_quiz(quiz_id=quiz_id, quiz_in=quiz_in, db=db)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[RequestedQuiz])
async def get_quizzes(respondent_id: int = None, db: AsyncSession = Depends(get_db)) -> list[Quiz]:
    """
    Get all quizzes or all respondent quizzes
    """

    if respondent_id is None:
        return await crud_quizzes.get_all_quizzes(db=db)

    quizzes_ids: list[int] = await crud_quiz_respondents.get_respondent_quizzes(respondent_id=respondent_id, db=db)

    quizzes: list[Quiz | None] = [None] * len(quizzes_ids)
    for i in range(len(quizzes_ids)):
        quizzes[i] = await crud_quizzes.get_quiz_by_id(quiz_id=quizzes_ids[i], db=db)

    return quizzes


@router.get('/{quiz_id}', status_code=status.HTTP_200_OK, response_model=RequestedQuiz)
async def get_quiz_by_id(quiz_id: int, db: AsyncSession = Depends(get_db)) -> Quiz | None:
    """
    Get quiz by id
    """

    is_valid: bool = await check_id_is_valid(model=Quiz, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz with this id has does not exist')

    return await crud_quizzes.get_quiz_by_id(quiz_id=quiz_id, db=db)


@router.get('/{quiz_id}/respondent/{respondent_id}')
async def has_access_to_quiz(quiz_id: int, respondent_id: int, db: AsyncSession = Depends(get_db)) -> bool:
    """
    Check has respondent access to quiz
    """
    pass


@router.post('/{quiz_id}/add/', status_code=status.HTTP_200_OK)
async def add_respondent_to_quiz(quiz_id: int, token: Annotated[str, Header()], db: AsyncSession = Depends(get_db)):
    pass
