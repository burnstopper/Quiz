from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.quiz import crud as crud_quizzes
from app.models.template import Template
from app.schemas.template import FullTemplate
from app.schemas.template import Template as TemplateWithTests
from app.utils.test_data import get_test_data, get_tests


async def get_template_with_tests(template: Template, tests_ids: list[int]) -> TemplateWithTests:
    requested_template = {'id': template.id,
                          'name': template.name,
                          'tests': [get_test_data(test_id=test_id) for test_id in tests_ids]}

    return TemplateWithTests(**requested_template)


async def get_full_template(template: Template, db: AsyncSession) -> FullTemplate:
    requested_template = {'id': template.id,
                          'name': template.name,
                          'quizzes': await crud_quizzes.get_quizzes_by_template_id(template_id=template.id, db=db),
                          'tests': await get_tests(template_id=template.id, db=db)}

    return FullTemplate(**requested_template)
