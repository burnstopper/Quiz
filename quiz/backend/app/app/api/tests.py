from fastapi import APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.template_test import TemplateTest
from app.utils.test_data import get_test_data, get_tests

router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[TemplateTest])
async def get_tests_names() -> list[TemplateTest]:
    """
    Get all tests
    """

    tests_ids: list[int] = [1, 2, 3, 4]  # push back 5 for questionnaire
    return [get_test_data(test_id=test_id) for test_id in tests_ids]


@router.get('/{template_id}', status_code=status.HTTP_200_OK, response_model=list[TemplateTest])
async def get_template_tests(template_id: int, db: AsyncSession) -> list[TemplateTest]:
    return await get_tests(template_id=template_id, db=db)
