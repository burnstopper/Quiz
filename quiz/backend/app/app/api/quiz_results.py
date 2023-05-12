from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.checkers import check_id_is_valid
from app.api.templates import get_tests

from app.core.config import settings

from app.crud.quiz import crud as crud_quizzes
from app.database.dependencies import get_db

from app.schemas.quiz_results import QuizResults
from app.schemas.template_test import TemplateTest, TemplateTestResults

router = APIRouter()


def parse_results_json(results_json: dict) -> list[TemplateTestResults]:
    keys: list[str] = list(results_json.keys())

    results: list[TemplateTestResults | None] = [None] * len(keys)
    for i in range(len(keys)):
        test = {'id': int(keys[i][-1]),
                'results': results_json[keys[i]]
                }

        results[i] = TemplateTestResults(**test)
    return results


async def get_quiz_results(quiz_id: int, db: AsyncSession, respondent_id: int = None) -> QuizResults:
    is_valid: bool = await check_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz with this id does not exist')

    quiz_template_id: int = (await crud_quizzes.get_quiz_by_id(quiz_id=quiz_id, db=db)).template_id
    tests: list[TemplateTest] = await get_tests(template_id=quiz_template_id, db=db)

    params = {'quiz_id': quiz_id,
              'test_ids': [test.id for test in tests],
              }

    if respondent_id is not None:
        params['respondent_id'] = respondent_id

    # sets retries amount to 10 and if after this Test microservice does not respond - raise normal exception (5xx)
    transport = httpx.AsyncHTTPTransport(retries=10)
    timeout = httpx.Timeout(1.0)
    async with httpx.AsyncClient(transport=transport, timeout=timeout) as client:

        response = await client.get(url=f'http://{settings.TEST_SERVICE_URL}/api/gateway/v1/tests_results/by-quiz',
                                    params=params,
                                    headers={'Authorization': f'Bearer {settings.TEST_SERVICES_BEARER_TOKEN}'}
                                    )

    tests_results = parse_results_json(results_json=response.json())
    return QuizResults(**{'quiz_id': quiz_id, 'tests_results': tests_results})


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[QuizResults])
async def get_quizzes_results(quizzes_ids: Annotated[list[int], Query()], respondent_id: int = None,
                              db: AsyncSession = Depends(get_db)) -> list[QuizResults]:
    results: list[QuizResults | None] = [None] * len(quizzes_ids)
    for i in range(len(quizzes_ids)):
        results[i] = await get_quiz_results(quiz_id=quizzes_ids[i], respondent_id=respondent_id, db=db)

    return results
