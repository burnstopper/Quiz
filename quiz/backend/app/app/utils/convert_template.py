from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.quiz import crud as crud_quizzes
from app.models.template import Template
from app.schemas.template import Template as RequestedTemplate
from app.utils.test_data import get_test_data, get_tests


async def get_requested_template(template: Template, tests_ids: list[int] = None,
                                 db: AsyncSession = None) -> RequestedTemplate:
    requested_template = {'id': template.id,
                          'name': template.name
                          }

    # db is None, when function is called from creat_template or update_template endpoint, because db is committed
    # In these cases we do not need quizzes of the template
    if db is None:
        requested_template['tests'] = [get_test_data(test_id=test_id) for test_id in tests_ids]
    else:
        requested_template['quizzes'] = await crud_quizzes.get_quizzes_by_template_id(template_id=template.id, db=db)
        requested_template['tests'] = await get_tests(template_id=template.id, db=db)

    return RequestedTemplate(**requested_template)
