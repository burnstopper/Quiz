from pydantic import BaseModel, Field

from app.schemas.template_test import TemplateTestResults


class QuizResultsBase(BaseModel):
    quiz_id: int = Field(ge=1)


class QuizResults(QuizResultsBase):
    tests_result: list[TemplateTestResults]


class QuizResultsStatus(QuizResultsBase):
    tests_status: bool
