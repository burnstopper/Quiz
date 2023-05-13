from app.core.config import settings
from app.schemas.template_test import TemplateTest


def check_test_id_is_valid(tests_ids: list[int]) -> bool:
    return all([0 < test_id <= settings.COUNT_TESTS_SERVICES for test_id in tests_ids])


def get_test_data(test_id: int) -> TemplateTest:
    match test_id:
        case 1:
            return TemplateTest(**{'id': 1, 'name': settings.BURNOUT_SERVICE_NAME, 'url': settings.BURNOUT_SERVICE_URL})
        case 2:
            return TemplateTest(**{'id': 2, 'name': settings.FATIGUE_SERVICE_NAME, 'url': settings.FATIGUE_SERVICE_URL})
        case 3:
            return TemplateTest(**{'id': 3, 'name': settings.COPING_SERVICE_NAME, 'url': settings.COPING_SERVICE_URL})
        case 4:
            return TemplateTest(**{'id': 4, 'name': settings.SPB_SERVICE_NAME, 'url': settings.SPB_SERVICE_URL})
