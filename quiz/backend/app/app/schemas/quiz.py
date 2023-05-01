from pydantic import BaseModel, Field


# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models
# not a @dataclass because dict() method is required in CRUD


class QuizBase(BaseModel):
    name: str = Field(min_length=1)
    description: str
    template_id: int = Field(ge=1)


class QuizCreate(QuizBase):
    pass


class Quiz(QuizBase):
    id: int = Field(ge=1)

    # https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
    class Config:
        orm_mode = True


class QuizUpdate(QuizCreate):
    pass
