from pydantic import BaseModel, Field


class TemplateTestBase(BaseModel):
    id: int = Field(ge=1)


class TemplateTest(TemplateTestBase):
    name: str = Field(min_length=1)
    url: str = Field(min_length=1)


class TemplateTestResults(TemplateTestBase):
    results: list[dict]
