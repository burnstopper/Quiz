from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.crud.quiz import crud as crud_quizzes
from app.crud.quiz_respondents import crud as crud_quiz_respondents
from app.database.dependencies import get_db
from app.schemas.quiz import QuizCreate, QuizUpdate
from app.schemas.quiz import Quiz as RequestedQuiz
from app.models.quiz import Quiz


async def check_is_quiz_name_unique(quiz_name: str, db: AsyncSession) -> bool:
    query = (
        select(Quiz.name)
        .where(Quiz.name == quiz_name.strip())
    )

    is_used_quiz_name: str | None = (await db.execute(query)).first()
    if is_used_quiz_name is not None:
        return False
    return True


async def check_there_are_conflicts_with_other_names(quiz_id: int, quiz_name: str, db: AsyncSession) -> bool:
    query = (
        select(Quiz.id)
        .where(Quiz.name == quiz_name.strip())
    )

    result_id: int = (await db.execute(query)).scalar()
    if result_id is None:
        return True
    elif result_id != quiz_id:
        return False
    return True


async def check_quiz_id_is_valid(quiz_id: int, db: AsyncSession) -> bool:
    query = (
        func.max(Quiz.id)
    )

    max_id: int = (await db.execute(query)).scalar()
    if max_id is None:
        max_id = 0
    return quiz_id <= max_id


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=RequestedQuiz)
async def create_quiz(quiz_in: QuizCreate, db: AsyncSession = Depends(get_db)) -> RequestedQuiz:
    """
    Create new quiz
    """

    if not check_is_quiz_name_unique(quiz_name=quiz_in.name, db=db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Quiz with this name has already been created')

    return await crud_quizzes.create_new_quiz(quiz_in=quiz_in, db=db)


@router.put('/{quiz_id}', status_code=status.HTTP_200_OK, response_model=RequestedQuiz)
async def update_quiz(quiz_id: int, quiz_in: QuizUpdate, db: AsyncSession = Depends(get_db)) -> RequestedQuiz:
    """
    Update quiz by id
    """

    if check_quiz_id_is_valid(quiz_id=quiz_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Quiz with this id has does not exist')

    if check_there_are_conflicts_with_other_names(quiz_id=quiz_id, quiz_name=quiz_in.name, db=db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Quiz with this name has already been created')

    return await crud_quizzes.update_quiz(quiz_id=quiz_id, quiz_in=quiz_in, db=db)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[RequestedQuiz])
async def get_all_quizzes(db: AsyncSession = Depends(get_db)) -> list[RequestedQuiz]:
    """
    Get all quizzes
    """

    return await crud_quizzes.get_all_quizzes(db=db)


@router.get('/{quiz_id}', status_code=status.HTTP_200_OK, response_model=RequestedQuiz)
async def get_quiz_by_id(quiz_id: int, db: AsyncSession = Depends(get_db)) -> Quiz | None:
    """
    Get quiz by id
    """

    if check_quiz_id_is_valid(quiz_id=quiz_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Quiz with this id has does not exist')

    return crud_quizzes.get_quiz_by_id(quiz_id=quiz_id, db=db)


@router.get('/{quiz_id}/respondent/{respondent_id}')
async def has_access_to_quiz(quiz_id: int, respondent_id: int, db: AsyncSession = Depends(get_db)) -> bool:
    """
    Check has respondent access to quiz
    """

    return await crud_quiz_respondents.check_access_to_quizz(quiz_id=quiz_id, respondent_id=respondent_id, db=db)
