from pydantic import BaseModel, Field


class QuizResultsBase(BaseModel):
    pass


class QuizResults(QuizResultsBase):
    quiz_id: int = Field(ge=1)
    results: list[dict[str, int]]
