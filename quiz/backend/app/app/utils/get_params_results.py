from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.template_test import TemplateTest
from app.crud.quiz import crud
from app.api.templates import get_tests


async def get_params(quiz_id: int, db: AsyncSession, respondent_id: int = None)->dict:
    quiz_template_id: int = (await crud.get_quiz_by_id(quiz_id=quiz_id, db=db)).template_id
    tests: list[TemplateTest] = await get_tests(template_id=quiz_template_id, db=db)

    params = {'quiz_id': quiz_id,
              'test_ids': [test.id for test in tests],
              }

    if respondent_id is not None:
        params['respondent_id'] = respondent_id
    return params
