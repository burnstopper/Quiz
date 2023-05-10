# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

from app.database.base_class import Base  # noqa
from app.models.quiz import Quiz  # noqa
from app.models.quiz_respondent import QuizRespondent  # noqa
from app.models.template import Template  # noqa
from app.models.template_test import TemplateTest  # noqa
