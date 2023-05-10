from pydantic import BaseModel, Field


class TemplateTestBase(BaseModel):
    pass


class TemplateTest(TemplateTestBase):
    id: int = Field(ge=1)
    name: str = Field(min_length=1)
    url: str = Field(min_length=1)
    bearer_token: str
