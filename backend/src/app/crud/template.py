from typing import Type

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.template_tests import crud as crud_template_tests
from app.models.template import Template
from app.schemas.template import Template as RequiredTemplate
from app.schemas.template import TemplateCreate


class CRUDTemplate:
    def __init__(self, model: Type[Template]):
        self.model = model

    async def is_unique_template_name(self, db: AsyncSession, template_name: str, template_id: int = None) -> bool:
        if template_id is None:
            query = (
                select(self.model.name)
                .where(self.model.name == template_name.strip())
            )

            has_template_name_added = (await db.execute(query)).scalar()
            if has_template_name_added is None:
                return True
            return False
        else:
            query = (
                select(self.model.id)
                .where(self.model.name == template_name.strip())
            )

            result_id: int = (await db.execute(query)).scalar()

            if result_id != template_id:
                return False
            return True

    async def get_max_template_id(self, db: AsyncSession) -> int:
        query = (
            func.max(self.model.id)
        )

        max_template_id: int = (await db.execute(query)).scalar()

        if max_template_id is None:
            return 0
        return max_template_id

    async def create_template(self, db: AsyncSession, template_in: TemplateCreate) -> str | None:
        is_unique: bool = await self.is_unique_template_name(db=db, template_name=template_in.name)

        # template with this name has been already created
        if not is_unique:
            return f'Template with {template_in.name} has already been created'

        max_template_id: int = await self.get_max_template_id(db=db)

        new_template = Template(name=template_in.name.strip())
        db.add(new_template)

        await crud_template_tests.add_tests_to_template(db=db,
                                                        template_id=max_template_id + 1,
                                                        tests=template_in.tests_ids,
                                                        )
        await db.commit()

    async def update_template(self, db: AsyncSession, template_id: int, template_in: RequiredTemplate):
        is_unique: bool = await self.is_unique_template_name(db=db,
                                                             template_name=template_in.name,
                                                             template_id=template_id)

        # template with this name has been already created
        if not is_unique:
            return f'Template with this name "{template_in.name}" has already been created'

        query = (
            update(self.model)
            .where(self.model.id == template_in.id)
            .values(name=template_in.name)
            .returning(Template)
        )

        await db.execute(query)

        await crud_template_tests.update_template_tests(db=db, template_id=template_id, tests=template_in.tests_ids)

        await db.commit()

    async def get_all_template(self, db: AsyncSession) -> list[RequiredTemplate]:
        query = (
            select(self.model.id, self.model.name)
        )

        template_ids_with_names = (await db.execute(query)).all()
        templates: list[None | RequiredTemplate] = [None] * len(template_ids_with_names)

        for i in range(len(template_ids_with_names)):
            id_, name = template_ids_with_names[i]

            templates[i] = await self.get_template_by_id(db=db, template_id=id_, template_name=name)

        return templates

    async def get_template_by_id(self, db: AsyncSession,
                                 template_id: int,
                                 template_name: str = None) -> (RequiredTemplate | None, str | None):

        max_template_id: int = await self.get_max_template_id(db=db)
        if template_id > max_template_id:
            return None, f'Template with this id does not exist'

        if template_name is None:
            query = (
                select(self.model.name)
                .where(self.model.id == template_id)
            )

            template_name = (await db.execute(query)).scalar()

        tests = await crud_template_tests.get_template_tests(db=db, template_id=template_id)

        template = {'id': template_id,
                    'name': template_name,
                    'tests_ids': [None] * len(tests)
                    }

        for j in range(len(tests)):
            index, test_id = tests[j].index, tests[j].test_id

            template['tests_ids'][index] = test_id

        return RequiredTemplate(**template)


crud = CRUDTemplate(Template)
