from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.quiz import crud as crud_quizzes
from app.crud.quiz_respondents import crud as crud_quiz_respondents
from app.crud.template import crud as crud_templates
from app.database.dependencies import get_db
from app.models.quiz import Quiz
from app.schemas.quiz import Quiz as RequestedQuiz
from app.schemas.quiz import QuizCreate, QuizUpdate
from app.utils.validators import check_conflicts_with_other_names
from app.utils.validators import check_item_id_is_valid, check_is_name_unique
from app.utils.validators import has_respondent_added_to_quiz

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=RequestedQuiz)
async def create_quiz(quiz_in: QuizCreate, db: AsyncSession = Depends(get_db)) -> Quiz:
    """
    Create a new quiz
    """
    is_valid: bool = await check_item_id_is_valid(crud=crud_templates, item_id=quiz_in.template_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Template with this id does not exist')

    is_unique: bool = await check_is_name_unique(crud=crud_quizzes, item_name=quiz_in.name, db=db)
    if not is_unique:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Quiz with this name already has been created')

    new_id: int = (await crud_quizzes.get_last_id(db=db)) + 1
    return await crud_quizzes.create_new_quiz(quiz_in=quiz_in, new_id=new_id, db=db)


@router.put('/{quiz_id}', status_code=status.HTTP_200_OK, response_model=RequestedQuiz)
async def update_quiz(quiz_id: int, quiz_in: QuizUpdate, db: AsyncSession = Depends(get_db)) -> Quiz:
    """
    Update the quiz by id
    """

    is_valid: bool = await check_item_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz with this id does not exist')

    is_unique: bool = await check_conflicts_with_other_names(crud=crud_quizzes, item_id=quiz_id, item_name=quiz_in.name,
                                                             db=db)
    if not is_unique:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Quiz with this name already has been created')

    return await crud_quizzes.update_quiz(quiz_id=quiz_id, quiz_in=quiz_in, db=db)


@router.get('/{quiz_id}', status_code=status.HTTP_200_OK, response_model=RequestedQuiz)
async def get_quiz_by_id(quiz_id: int, db: AsyncSession = Depends(get_db)) -> Quiz:
    """
    Get the quiz by id
    """

    is_valid: bool = await check_item_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz with this id does not exist')

    return await crud_quizzes.get_quiz_by_id(quiz_id=quiz_id, db=db)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[RequestedQuiz])
async def get_quizzes(respondent_id: int = None, db: AsyncSession = Depends(get_db)) -> list[Quiz]:
    """
    Get all existing quizzes or all respondent quizzes
    """

    if respondent_id is None:
        return await crud_quizzes.get_all_quizzes(db=db)

    respondent_quizzes_ids: list[int] = await crud_quiz_respondents.get_respondent_quizzes(respondent_id=respondent_id,
                                                                                           db=db)

    quizzes: list[Quiz | None] = [None] * len(respondent_quizzes_ids)
    for i in range(len(respondent_quizzes_ids)):
        quizzes[i] = await crud_quizzes.get_quiz_by_id(quiz_id=respondent_quizzes_ids[i], db=db)

    return quizzes


@router.get('/{quiz_id}/respondents', status_code=status.HTTP_200_OK, response_class=JSONResponse)
async def get_quiz_respondents(quiz_id: int, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """
    Get quiz respondents
    """

    is_valid: bool = await check_item_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz with this id does not exist')

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            'respondents': await crud_quiz_respondents.get_quiz_respondents(quiz_id=quiz_id, db=db)
                        })


@router.get('/{quiz_id}/check_access', status_code=status.HTTP_200_OK, response_class=JSONResponse)
async def has_access_to_quiz(quiz_id: int, respondent_id: int, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """
    Check has the respondent access to quiz
    """

    is_valid: bool = await check_item_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz with this id does not exist')

    has_access: bool = await has_respondent_added_to_quiz(quiz_id=quiz_id,
                                                          respondent_id=respondent_id,
                                                          db=db)

    return JSONResponse(status_code=status.HTTP_200_OK, content={'has_access': has_access})
