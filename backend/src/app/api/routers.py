from fastapi import APIRouter

from app.api.quizzes import router as quizzes_router
from app.api.templates import router as template_router
from app.api.token import router as token_router

api_router = APIRouter()

api_router.include_router(quizzes_router,
                          prefix='/api/quizzes',
                          tags=['Quiz']
                          )

api_router.include_router(template_router,
                          prefix='/api/templates',
                          tags=['Template'])

api_router.include_router(token_router,
                          prefix='/api/token',
                          tags=['Token'])