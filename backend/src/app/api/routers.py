from fastapi import APIRouter

from app.api.quizzes import router as quizzes_router
from app.api.templates import router as template_router

api_router = APIRouter()

api_router.include_router(quizzes_router,
                          prefix='/quizzes',
                          tags=['Quiz']
                          )

api_router.include_router(template_router,
                          prefix='/templates',
                          tags=['Template'])
