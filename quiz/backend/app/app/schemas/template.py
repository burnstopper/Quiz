from pydantic import BaseModel, Field

from app.schemas.quiz import Quiz
from app.schemas.template_test import TemplateTest


# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models
# not a @dataclass because dict() method is required in CRUD


class TemplateBase(BaseModel):
    name: str = Field(min_length=1)


class TemplateCreate(TemplateBase):
    tests_ids: list[int]


class Template(TemplateBase):
    id: int = Field(ge=1)
    tests: list[TemplateTest] | None


class FullTemplate(Template):
    quizzes: list[Quiz] | None

    # https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
    class Config:
        orm_mode = True


class TemplateUpdate(TemplateCreate):
    pass
