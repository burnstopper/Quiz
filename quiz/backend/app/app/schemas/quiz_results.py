from pydantic import BaseModel, Field

from app.schemas.template_test import TemplateTestResults


class QuizResultsBase(BaseModel):
    pass


class QuizResults(QuizResultsBase):
    quiz_id: int = Field(ge=1)
    tests_results: list[TemplateTestResults]
