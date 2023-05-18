from fastapi import APIRouter, Depends

from app.api.invite import router as invite_router
from app.api.quiz_results import router as results_router
from app.api.quizzes import router as quizzes_router
from app.api.templates import router as template_router
from app.api.tests import router as tests_router
from app.api.token import router as token_router
from app.database.dependencies import get_db

api_router = APIRouter()

api_router.include_router(quizzes_router,
                          prefix='/api/quizzes',
                          dependencies=[Depends(get_db)],
                          tags=['Quiz']
                          )

api_router.include_router(invite_router,
                          prefix='/invite/quizzes',
                          dependencies=[Depends(get_db)],
                          tags=['Invite']
                          )

api_router.include_router(template_router,
                          prefix='/api/templates',
                          dependencies=[Depends(get_db)],
                          tags=['Template'])

api_router.include_router(tests_router,
                          prefix='/api/tests',
                          dependencies=[Depends(get_db)],
                          tags=['Test'])

api_router.include_router(results_router,
                          prefix='/api/results',
                          tags=['Results'])

api_router.include_router(token_router,
                          prefix='/api/token',
                          tags=['Token'])
