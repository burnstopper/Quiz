from typing import Type

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.template_tests import TemplateTests


class CRUDTemplateTests:
    def __init__(self, model: Type[TemplateTests]):
        self.model = model

    async def add_tests_to_template(self, template_id: int, tests: list[int], db: AsyncSession):
        template_tests = [TemplateTests(template_id=template_id,
                                        index=i,
                                        test_id=tests[i]
                                        ) for i in range(len(tests))
                          ]

        db.add_all(template_tests)
        await db.commit()

    async def update_template_tests(self, template_id: int, tests: list[int], db: AsyncSession):
        query = (
            delete(self.model)
            .where(self.model.template_id == template_id)
        )

        await db.execute(query)

        await self.add_tests_to_template(template_id=template_id, tests=tests, db=db)

    async def get_template_tests(self, template_id: int, db: AsyncSession) -> list[TemplateTests]:
        query = (
            select(self.model)
            .where(self.model.template_id == template_id)
        )

        return list((await db.execute(query)).scalars().all())


crud = CRUDTemplateTests(TemplateTests)
