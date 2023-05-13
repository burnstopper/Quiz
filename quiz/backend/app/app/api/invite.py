import json
from typing import Annotated

from fastapi import APIRouter, Header, Depends, status, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.token import get_respondent_id_by_token
from app.utils.checkers import check_item_id_is_valid
from app.crud.quiz import crud as crud_quizzes
from app.crud.quiz_respondents import crud as crud_quiz_respondents
from app.crud.quiz_respondents import has_respondent_added_to_quiz
from app.database.dependencies import get_db

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
async def add_respondent_to_quiz(quiz_id: int, respondent_token: Annotated[str, Header()],
                                 db: AsyncSession = Depends(get_db)):
    is_valid: bool = await check_item_id_is_valid(crud=crud_quizzes, item_id=quiz_id, db=db)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid invite link: quiz with this id does not exist')

    respondent_id: int = json.loads((await get_respondent_id_by_token(respondent_token)).body)['respondent_id']
    has_added: bool = await has_respondent_added_to_quiz(crud_quiz_respondents=crud_quiz_respondents, quiz_id=quiz_id,
                                                         respondent_id=respondent_id,
                                                         db=db)

    if has_added:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Respondent has already added to quiz')

    await crud_quiz_respondents.add_respondent(quiz_id=quiz_id, respondent_id=respondent_id, db=db)
