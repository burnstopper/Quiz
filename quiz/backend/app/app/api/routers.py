from fastapi import APIRouter, Depends

from app.api.quizzes import router as quizzes_router
from app.api.templates import router as template_router
from app.api.token import router as token_router
from app.database.dependencies import get_db

api_router = APIRouter()

api_router.include_router(quizzes_router,
                          prefix='/api/quizzes',
                          dependencies=[Depends(get_db)],
                          tags=['Quiz']
                          )

api_router.include_router(template_router,
                          prefix='/api/templates',
                          dependencies=[Depends(get_db)],
                          tags=['Template'])

api_router.include_router(token_router,
                          prefix='/api/token',
                          tags=['Token'])
