from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateUpdate


class CRUDTemplate(CRUDBase[Template]):
    async def create_template(self, template_in: TemplateCreate, db: AsyncSession) -> Template:
        new_template = Template(name=template_in.name.strip())
        db.add(new_template)

        return new_template

    async def update_template(self, template_id: int, template_in: TemplateUpdate, db: AsyncSession) -> Template:
        query = (
            update(self.model)
            .where(self.model.id == template_id)
            .values(name=template_in.name)
            .returning(Template)
        )

        return (await db.execute(query)).scalar()

    async def get_all_templates(self, db: AsyncSession) -> list[Template]:
        query = (
            select(self.model)
        )

        return list((await db.execute(query)).scalars().all())

    async def get_template_by_id(self, template_id: int, db: AsyncSession) -> Template:
        query = (
            select(self.model)
            .where(self.model.id == template_id)
        )

        return (await db.execute(query)).scalar()


crud = CRUDTemplate(Template)
