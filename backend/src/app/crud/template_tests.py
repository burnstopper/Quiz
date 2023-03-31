from typing import Type

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.template_tests import TemplateTests


class CRUDTemplateTests:
    def __init__(self, model: Type[TemplateTests]):
        self.model = model

    async def add_tests_to_template(self, db: AsyncSession, template_id: int, tests: list[int]):
        template_tests = [TemplateTests(template_id=template_id,
                                        index=i,
                                        test_id=tests[i]
                                        ) for i in range(len(tests))
                          ]

        db.add_all(template_tests)

    async def delete_template_tests(self, db: AsyncSession, template_id: int):
        query = (
            delete(self.model)
            .where(self.model.template_id == template_id)
        )

        await db.execute(query)

    async def update_template_tests(self, db: AsyncSession, template_id: int, tests: list[int]):
        await self.delete_template_tests(db=db, template_id=template_id)

        await self.add_tests_to_template(db=db, template_id=template_id, tests=tests)

    async def get_template_tests(self, db: AsyncSession, template_id: int) -> list[TemplateTests]:
        query = (
            select(self.model)
            .where(self.model.template_id == template_id)
        )

        return list((await db.execute(query)).scalars().all())


crud = CRUDTemplateTests(TemplateTests)
