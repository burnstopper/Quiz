from typing import Annotated

from fastapi import APIRouter, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.template import Template
from app.schemas.template_test import TemplateTest
from app.utils.test_data import get_test_data, get_tests

router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[TemplateTest])
async def get_tests_data() -> list[TemplateTest]:
    """
    Get all tests
    """

    tests_ids: list[int] = [1, 2, 3, 4, 5]  # push back 5 for questionnaire
    return [get_test_data(test_id=test_id) for test_id in tests_ids]

