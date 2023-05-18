from pydantic import BaseModel, Field
from app.core.config import settings


# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models
# not a @dataclass because dict() method is required in CRUD


class QuizBase(BaseModel):
    pass


class QuizCreate(QuizBase):
    name: str = Field(min_length=1)
    description: str
    template_id: int = Field(ge=1)


class Quiz(QuizCreate):
    id: int = Field(ge=1)
    invite_link: str = Field(regex=f'http://{settings.HOST}:{settings.PORT}/invite/quizzes/\d/add')

    # https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
    class Config:
        orm_mode = True


class QuizUpdate(QuizCreate):
    pass
