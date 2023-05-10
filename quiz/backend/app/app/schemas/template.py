from pydantic import BaseModel, Field

from app.schemas.quiz import Quiz


# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models
# not a @dataclass because dict() method is required in CRUD


class TemplateBase(BaseModel):
    pass


class TemplateCreate(TemplateBase):
    name: str = Field(min_length=1)
    tests_ids: list[int]


class Template(TemplateCreate):
    id: int = Field(ge=1)
    tests_names: list[str] | None
    tests_urls: list[str] | None
    quizzes: list[Quiz] | None

    # https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
    class Config:
        orm_mode = True


class TemplateUpdate(TemplateCreate):
    pass
