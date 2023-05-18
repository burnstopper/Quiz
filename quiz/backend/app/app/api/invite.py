import json

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.quizzes import has_access_to_quiz
from app.crud.quiz import crud as crud_quizzes
from app.crud.quiz_respondents import crud as crud_quiz_respondents
from app.database.dependencies import get_db
from app.utils.validators import check_item_id_is_valid

router = APIRouter()


@router.get('/{quiz_id}/add', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_html_page(quiz_id: int, db: AsyncSession = Depends(get_db)) -> HTMLResponse:
    is_valid: bool = await check_item_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid invite link: quiz with this id does not exist')

    html_content = """
    <html>
        <body>
            <h1>Loading...</h1>
        </body>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)


@router.post('/{quiz_id}/add', status_code=status.HTTP_200_OK)
async def add_respondent_to_quiz(quiz_id: int, respondent_id: int, db: AsyncSession = Depends(get_db)):
    is_valid: bool = await check_item_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid invite link: quiz with this id does not exist')

    has_added: bool = json.loads((await has_access_to_quiz(quiz_id=quiz_id,
                                                           respondent_id=respondent_id,
                                                           db=db)).body)['has_access']

    if has_added:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Respondent has already added to quiz')

    await crud_quiz_respondents.add_respondent(quiz_id=quiz_id, respondent_id=respondent_id, db=db)
