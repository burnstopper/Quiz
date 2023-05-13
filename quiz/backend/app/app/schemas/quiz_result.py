from pydantic import BaseModel, Field

from app.schemas.template_test import TemplateTestResults


class QuizResultBase(BaseModel):
    quiz_id: int = Field(ge=1)


class QuizResult(QuizResultBase):
    tests_result: list[TemplateTestResults]


class QuizResultStatus(QuizResultBase):
    tests_status: bool
