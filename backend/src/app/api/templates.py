from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.crud.template import crud
from app.database.dependencies import get_db
from app.schemas.template import TemplateCreate, Template, TemplateUpdate

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_template(template_in: TemplateCreate, db: Session = Depends(get_db)):
    """
    Create template
    """

    error: None | str = await crud.create_template(db=db, template_in=template_in)
    if error is not None:
        raise HTTPException(status_code=409, detail=error)


@router.put('/{template_id}', status_code=status.HTTP_200_OK)
async def update_template(template_id: int, template_in: TemplateUpdate, db: Session = Depends(get_db)):
    """
    Update template by id
    """

    error: None | str = await crud.update_template(db=db, template_in=template_in)
    if error is not None:
        raise HTTPException(status_code=409, detail=error)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[Template])
async def get_all_templates(db: Session = Depends(get_db)):
    """
    Get all existing templates
    """

    return await crud.get_all_template(db=db)


@router.get('/{template_id}', status_code=status.HTTP_200_OK, response_model=Template)
async def get_template_by_id(template_id: int, db: Session = Depends(get_db)) -> Template:
    """
    Get template by id
    """

    template: None | Template
    error: None | str

    template, error = crud.get_template_by_id(db=db, template_id=template_id)
    if error is not None:
        raise HTTPException(status_code=409, detail=error)

    return template
