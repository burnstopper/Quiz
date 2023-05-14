from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.template import crud as crud_templates
from app.crud.template_tests import crud as crud_template_tests
from app.database.dependencies import get_db
from app.models.template import Template
from app.schemas.template import Template as RequestedTemplate
from app.schemas.template import TemplateCreate, TemplateUpdate
from app.utils.validators import check_is_name_unique, check_item_id_is_valid, check_conflicts_with_other_names
from app.utils.test_data import check_test_id_is_valid
from app.utils.convert_template import get_requested_template

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=RequestedTemplate)
async def create_template(template_in: TemplateCreate, db: AsyncSession = Depends(get_db)) -> RequestedTemplate:
    """
    Create a new template
    """

    is_unique: bool = await check_is_name_unique(crud=crud_templates, item_name=template_in.name, db=db)
    if not is_unique:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Template with this name has already been created')

    is_valid_tests_ids: bool = check_test_id_is_valid(tests_ids=template_in.tests_ids)
    if not is_valid_tests_ids:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Invalid test id')

    new_template: Template = await crud_templates.create_template(template_in=template_in, db=db)
    new_id: int = (await crud_templates.get_last_id(db=db)) + 1
    await crud_template_tests.add_tests_to_template(template_id=new_id, tests=template_in.tests_ids, db=db)

    return await get_requested_template(template=new_template, tests_ids=template_in.tests_ids)


@router.put('/{template_id}', status_code=status.HTTP_200_OK, response_model=RequestedTemplate)
async def update_template(template_id: int, template_in: TemplateUpdate,
                          db: AsyncSession = Depends(get_db)) -> RequestedTemplate:
    """
    Update the template by id
    """

    is_valid: bool = await check_item_id_is_valid(crud=crud_templates, item_id=template_id, db=db)
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

    return await get_requested_template(template=updated_template, tests_ids=template_in.tests_ids)


@router.get('/{template_id}', status_code=status.HTTP_200_OK, response_model=RequestedTemplate)
async def get_template_by_id(template_id: int, db: AsyncSession = Depends(get_db)) -> RequestedTemplate:
    """
    Get the template by id
    """

    is_valid: bool = await check_item_id_is_valid(crud=crud_templates, item_id=template_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Template with this id does not exist')

    template: Template = await crud_templates.get_template_by_id(template_id=template_id, db=db)

    return await get_requested_template(template=template, db=db)


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
