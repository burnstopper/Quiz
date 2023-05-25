from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.quiz import crud as crud_quizzes
from app.database.dependencies import get_db
from app.schemas.quiz_results import QuizResults, QuizResultsStatus
from app.utils.get_params_and_parse_results import get_params, parse_results_json
from app.utils.validators import check_item_id_is_valid

router = APIRouter()


@router.get('/{quiz_id}/status', status_code=status.HTTP_200_OK, response_model=QuizResultsStatus)
async def get_quiz_results_status(quiz_id: int, respondent_id: int = None,
                                  db: AsyncSession = Depends(get_db)) -> QuizResultsStatus:
    """
    Get result status of quiz by id
    """

    is_valid: bool = await check_item_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz with this id does not exist')

    params = await get_params(quiz_id=quiz_id, respondent_id=respondent_id, db=db)

    # sets retries amount to 10 and if after this Test microservice does not respond - raise normal exception (5xx)
    transport = httpx.AsyncHTTPTransport(retries=10)
    timeout = httpx.Timeout(1.0)
    async with httpx.AsyncClient(transport=transport, timeout=timeout) as client:
        response = await client.get(url=f'http://{settings.TEST_SERVICE_URL}/api/gateway/v1/results/exists',
                                    params=params,
                                    headers={'Authorization': f'Bearer {settings.TEST_SERVICES_BEARER_TOKEN}'}
                                    )

    return QuizResultsStatus(**{'quiz_id': quiz_id, 'tests_status': response.content, 'respondent_id': respondent_id})


@router.get('/{quiz_id}', status_code=status.HTTP_200_OK, response_model=QuizResults)
async def get_quiz_results(quiz_id: int, respondent_id: int = None, db: AsyncSession = Depends(get_db)) -> QuizResults:
    """
    Get result of quiz by id
    """

    is_valid: bool = await check_item_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz with this id does not exist')

    params = await get_params(quiz_id=quiz_id, respondent_id=respondent_id, db=db)

    # sets retries amount to 10 and if after this Test microservice does not respond - raise normal exception (5xx)
    transport = httpx.AsyncHTTPTransport(retries=10)
    timeout = httpx.Timeout(1.0)
    async with httpx.AsyncClient(transport=transport, timeout=timeout) as client:
        response = await client.get(url=f'http://{settings.TEST_SERVICE_URL}/api/gateway/v1/results/by-quiz',
                                    params=params,
                                    headers={'Authorization': f'Bearer {settings.TEST_SERVICES_BEARER_TOKEN}'}
                                    )

    tests_results = parse_results_json(results_json=response.json())
    return QuizResults(**{'quiz_id': quiz_id, 'tests_result': tests_results, 'respondent_id': respondent_id})


@router.get('/status/', status_code=status.HTTP_200_OK, response_model=list[QuizResultsStatus])
async def get_quizzes_results_status(quizzes_ids: Annotated[list[int], Query()], respondent_id: int = None,
                                     db: AsyncSession = Depends(get_db)) -> list[QuizResultsStatus]:
    """
    Get result status of quizzes
    """

    results_status: list[QuizResultsStatus | None] = [None] * len(quizzes_ids)
    for i in range(len(quizzes_ids)):
        results_status[i] = await get_quiz_results_status(quiz_id=quizzes_ids[i], respondent_id=respondent_id, db=db)
    return results_status


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[QuizResults])
async def get_quizzes_results(quizzes_ids: Annotated[list[int], Query()], respondent_id: int = None,
                              db: AsyncSession = Depends(get_db)) -> list[QuizResults]:
    """
    Get result of quizzes
    """

    results: list[QuizResults | None] = [None] * len(quizzes_ids)
    for i in range(len(quizzes_ids)):
        results[i] = await get_quiz_results(quiz_id=quizzes_ids[i], respondent_id=respondent_id, db=db)

    return results
