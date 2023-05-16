from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.quiz import crud as crud_quizzes
from app.database.dependencies import get_db
from app.schemas.quiz_result import QuizResult, QuizResultStatus
from app.utils.validators import check_item_id_is_valid
from app.utils.get_params_and_parse_results import get_params, parse_results_json

router = APIRouter()


@router.get('/{quiz_id}/status', status_code=status.HTTP_200_OK, response_model=QuizResultStatus)
async def get_quiz_result_status(quiz_id: int, respondent_id: int = None,
                                 db: AsyncSession = Depends(get_db)) -> QuizResultStatus:
    """
    Get result status of quiz by id
    """

    is_valid: bool = await check_item_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz with this id does not exist')

    # sets retries amount to 10 and if after this Test microservice does not respond - raise normal exception (5xx)
    transport = httpx.AsyncHTTPTransport(retries=10)
    timeout = httpx.Timeout(1.0)
    async with httpx.AsyncClient(transport=transport, timeout=timeout) as client:
        response = await client.get(url=f'http://{settings.TEST_SERVICE_URL}/api/gateway/v1/results/exists',
                                    params=await get_params(quiz_id=quiz_id, respondent_id=respondent_id, db=db),
                                    headers={'Authorization': f'Bearer {settings.TEST_SERVICES_BEARER_TOKEN}'}
                                    )

    return QuizResultStatus(**{'quiz_id': quiz_id, 'tests_status': response.content})


@router.get('/{quiz_id}', status_code=status.HTTP_200_OK, response_model=QuizResult)
async def get_quiz_result(quiz_id: int, respondent_id: int = None, db: AsyncSession = Depends(get_db)) -> QuizResult:
    """
    Get result of quiz by id
    """

    is_valid: bool = await check_item_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz with this id does not exist')

    # sets retries amount to 10 and if after this Test microservice does not respond - raise normal exception (5xx)
    transport = httpx.AsyncHTTPTransport(retries=10)
    timeout = httpx.Timeout(1.0)
    async with httpx.AsyncClient(transport=transport, timeout=timeout) as client:
        response = await client.get(url=f'http://{settings.TEST_SERVICE_URL}/api/gateway/v1/results/by-quiz',
                                    params=await get_params(quiz_id=quiz_id, respondent_id=respondent_id, db=db),
                                    headers={'Authorization': f'Bearer {settings.TEST_SERVICES_BEARER_TOKEN}'}
                                    )

    tests_result = parse_results_json(results_json=response.json())
    return QuizResult(**{'quiz_id': quiz_id, 'tests_result': tests_result})


@router.get('/status', status_code=status.HTTP_200_OK, response_model=list[QuizResultStatus])
async def get_quizzes_result_status(quizzes_ids: Annotated[list[int], Query()], respondent_id: int = None,
                                    db: AsyncSession = Depends(get_db)) -> list[QuizResultStatus]:
    """
    Get result status of quizzes
    """

    result_status: list[QuizResultStatus | None] = [None] * len(quizzes_ids)
    for i in range(len(quizzes_ids)):
        result_status[i] = await get_quiz_result_status(quiz_id=quizzes_ids[i], respondent_id=respondent_id, db=db)
    return result_status


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[QuizResult])
async def get_quizzes_result(quizzes_ids: Annotated[list[int], Query()], respondent_id: int = None,
                             db: AsyncSession = Depends(get_db)) -> list[QuizResult]:
    """
    Get result of quizzes
    """

    result: list[QuizResult | None] = [None] * len(quizzes_ids)
    for i in range(len(quizzes_ids)):
        result[i] = await get_quiz_result(quiz_id=quizzes_ids[i], respondent_id=respondent_id, db=db)

    return result
