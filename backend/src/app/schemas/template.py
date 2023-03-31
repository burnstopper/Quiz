from pydantic import BaseModel, Field


# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models
# not a @dataclass because dict() method is required in CRUD


class TemplateBase(BaseModel):
    name: str = Field(min_length=1)


class TemplateCreate(TemplateBase):
    tests_ids: list[int]


class Template(TemplateCreate):
    id: int = Field(ge=1)
    tests_names: list[str] | None

    # https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
    class Config:
        orm_mode = True


class TemplateUpdate(Template):
    pass
