from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.crud.quiz import crud
from app.crud.quiz_respondents import crud
from app.database.dependencies import get_db
from app.schemas.quiz import QuizCreate, Quiz, QuizUpdate

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_quiz(quiz_in: QuizCreate, db: Session = Depends(get_db)):
    """
    Create new quiz
    """

    error: str | None = await crud.create_new_quiz(db=db, quiz_in=quiz_in)
    if error is not None:
        raise HTTPException(status_code=409, detail=error)


@router.put('/', status_code=status.HTTP_200_OK)
async def update_quiz(quiz_in: QuizUpdate, db: Session = Depends(get_db)):
    """
    Update quiz by id
    """

    error: str | None = await crud.update_quiz(db=db, quiz_in=quiz_in)
    if error is not None:
        raise HTTPException(status_code=409, detail=error)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[Quiz])
async def get_quizzes(respondent_id: int = None, db: Session = Depends(get_db)) -> list[Quiz]:
    """
    Get all quizzes or quizzes for the respondent
    """

    if respondent_id is None:
        return await crud.get_all_quizzes(db=db)

    # respondent_quizzes = await crud.get_quizzes_by_respondent_id(db=db, respondent_id=respondent_id)
    #
    # return await crud.get_quizzes_by_respondent_id(db=db, quizzes_id=respondent_quizzes)


@router.get('/{quiz_id}', status_code=status.HTTP_200_OK, response_model=Quiz)
async def get_quiz_by_id(quiz_id: int, db: Session = Depends(get_db)) -> Quiz | None:
    """
    Get quiz by id
    """

    quiz: Quiz | None
    error: str | None

    quiz, error = await crud.get_quiz_by_id(db, quiz_id=quiz_id)
    if error is not None:
        raise HTTPException(status_code=409, detail=error)

    return quiz


@router.get('/{quiz_id}/respondent/{respondent_id}')
async def has_access_to_quiz(quiz_id: int, respondent_id: int, db: Session = Depends(get_db)) -> bool:
    """
    Check has respondent access to quiz
    """

    return await crud.check_access_to_quizz(db=db, quiz_id=quiz_id, respondent_id=respondent_id)
