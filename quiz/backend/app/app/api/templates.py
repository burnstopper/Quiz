from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.checkers import check_is_name_unique, check_id_is_valid, check_conflicts_with_other_names
from app.api.get_tests import get_tests, get_test_data
from app.crud.quiz import crud as crud_quizzes
from app.crud.template import crud as crud_templates
from app.crud.template_test import crud as crud_template_tests
from app.database.dependencies import get_db
from app.models.quiz import Quiz
from app.models.template import Template
from app.schemas.template import Template as RequestedTemplate
from app.schemas.template import TemplateCreate, TemplateUpdate
from app.schemas.template_test import TemplateTest

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=RequestedTemplate)
async def create_template(template_in: TemplateCreate, db: AsyncSession = Depends(get_db)) -> RequestedTemplate | None:
    """
    Create a new template
    """

    is_unique: bool = await check_is_name_unique(crud=crud_templates, item_name=template_in.name, db=db)
    if not is_unique:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Template with this name has already been created')

    new_template: Template = await crud_templates.create_template(template_in=template_in, db=db)

    new_id: int = (await crud_templates.get_last_id(db=db)) + 1

    await crud_template_tests.add_tests_to_template(template_id=new_id, tests=template_in.tests_ids, db=db)

    tests: list[TemplateTest] = [get_test_data(test_id=test_id) for test_id in template_in.tests_ids]

    return RequestedTemplate(**{'id': new_id,
                                'name': new_template.name,
                                'tests_ids': template_in.tests_ids,
                                'tests_names': [test.name for test in tests],
                                'tests_urls': [test.url for test in tests]
                                }
                             )


@router.put('/{template_id}', status_code=status.HTTP_200_OK, response_model=RequestedTemplate)
async def update_template(template_id: int, template_in: TemplateUpdate,
                          db: AsyncSession = Depends(get_db)) -> RequestedTemplate | None:
    """
    Update the template by id
    """

    is_valid: bool = await check_id_is_valid(crud=crud_templates, item_id=template_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Template with this id does not exist')

    is_unique: bool = await check_conflicts_with_other_names(crud=crud_templates, item_id=template_id,
                                                             item_name=template_in.name, db=db)
    if not is_unique:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Template with this name has already been created')

    updated_template: Template = await crud_templates.update_template(template_id=template_id, template_in=template_in,
                                                                      db=db)

    await crud_template_tests.update_template_tests(template_id=template_id, tests=template_in.tests_ids, db=db)

    tests: list[TemplateTest] = [get_test_data(test_id=test_id) for test_id in template_in.tests_ids]

    return RequestedTemplate(**{'id': updated_template.id,
                                'name': updated_template.name,
                                'tests_ids': template_in.tests_ids,
                                'tests_names': [test.name for test in tests],
                                'tests_urls': [test.url for test in tests]
                                }
                             )


@router.get('/{template_id}', status_code=status.HTTP_200_OK, response_model=RequestedTemplate)
async def get_template_by_id(template_id: int, db: AsyncSession = Depends(get_db)) -> RequestedTemplate | None:
    """
    Get the template by id
    """

    is_valid: bool = await check_id_is_valid(crud=crud_templates, item_id=template_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Template with this id does not exist')

    template: Template = await crud_templates.get_template_by_id(template_id=template_id, db=db)

    quizzes: list[Quiz] = await crud_quizzes.get_quizzes_by_template_id(template_id=template_id, db=db)

    tests: list[TemplateTest] = await get_tests(template_id=template_id, db=db)

    return RequestedTemplate(**{'id': template_id,
                                'name': template.name,
                                'tests_ids': [test.id for test in tests],
                                'tests_names': [test.name for test in tests],
                                'tests_urls': [test.url for test in tests],
                                'quizzes': quizzes
                                })


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[RequestedTemplate])
async def get_all_templates(db: AsyncSession = Depends(get_db)) -> list[RequestedTemplate]:
    """
    Get all existing templates
    """

    templates: list[Template] = await crud_templates.get_all_templates(db=db)

    results: list[RequestedTemplate | None] = [None] * len(templates)

    for i in range(len(templates)):
        results[i] = await get_template_by_id(template_id=templates[i].id, db=db)

    return results
