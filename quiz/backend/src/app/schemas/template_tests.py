from pydantic import BaseModel, Field


# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models
# not a @dataclass because dict() method is required in CRUD


class TemplateTestsBase(BaseModel):
    pass


class TemplateTest(TemplateTestsBase):
    test_id: int = Field(ge=1)
    index: int = Field(ge=0)
    template_id: int = Field(ge=1)

    # https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
    class Config:
        orm_mode = True
