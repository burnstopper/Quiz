from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.template_tests import crud as crud_template_tests
from app.models.template_test import TemplateTest
from app.schemas.template_test import TemplateTest as Test


def check_test_id_is_valid(tests_ids: list[int]) -> bool:
    return all([0 < test_id <= settings.COUNT_TESTS_SERVICES for test_id in tests_ids])


def get_test_data(test_id: int) -> Test:
    match test_id:
        case 1:
            return Test(**{'id': 1, 'name': settings.BURNOUT_SERVICE_NAME, 'url': settings.BURNOUT_SERVICE_URL})
        case 2:
            return Test(**{'id': 2, 'name': settings.FATIGUE_SERVICE_NAME, 'url': settings.FATIGUE_SERVICE_URL})
        case 3:
            return Test(**{'id': 3, 'name': settings.COPING_SERVICE_NAME, 'url': settings.COPING_SERVICE_URL})
        case 4:
            return Test(**{'id': 4, 'name': settings.SPB_SERVICE_NAME, 'url': settings.SPB_SERVICE_URL})
        case 5:
            return Test(
                **{'id': 5, 'name': settings.QUESTIONNAIRE_SERVICE_NAME, 'url': settings.QUESTIONNAIRE_SERVICE_URL}
            )


async def get_tests(template_id: int, db: AsyncSession) -> list[Test]:
    temp_tests: list[TemplateTest] = await crud_template_tests.get_template_tests(template_id=template_id, db=db)

    tests: list[Test | None] = [None] * len(temp_tests)
    for test in temp_tests:
        tests[test.index] = get_test_data(test_id=test.test_id)

    return tests
