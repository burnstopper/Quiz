from pydantic import BaseModel, Field

from app.schemas.template_test import TemplateTestResults


class QuizResultsBase(BaseModel):
    respondent_id: int | None
    quiz_id: int = Field(ge=1)


class QuizResults(QuizResultsBase):
    tests_result: list[TemplateTestResults]


class QuizResultsStatus(QuizResultsBase):
    respondent_id: int | None
    tests_status: bool
