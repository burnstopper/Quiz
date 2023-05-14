from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.quiz import crud
from app.schemas.template_test import TemplateTest
from app.schemas.template_test import TemplateTestResults as Result
from app.utils.test_data import get_tests


async def get_params(quiz_id: int, db: AsyncSession, respondent_id: int = None) -> dict:
    quiz_template_id: int = (await crud.get_quiz_by_id(quiz_id=quiz_id, db=db)).template_id
    tests: list[TemplateTest] = await get_tests(template_id=quiz_template_id, db=db)

    params = {'quiz_id': quiz_id,
              'test_ids': [test.id for test in tests],
              }

    if respondent_id is not None:
        params['respondent_id'] = respondent_id
    return params


def parse_results_json(results_json: dict) -> list[Result]:
    keys: list[str] = list(results_json.keys())

    results: list[Result | None] = [None] * len(keys)
    for i in range(len(keys)):
        test = {'id': int(keys[i][-1]),
                'results': results_json[keys[i]]
                }

        results[i] = Result(**test)
    return results
