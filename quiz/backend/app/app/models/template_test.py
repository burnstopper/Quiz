from sqlalchemy import Integer, Column

from app.database.base_class import Base


# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-models
# no need for __tablename__ because of declarative style (app.database.base_class)
class TemplateTest(Base):
    template_id = Column(Integer, primary_key=True, nullable=False)
    index = Column(Integer, nullable=False)
    test_id = Column(Integer, primary_key=True, nullable=False)

    def __repr__(self) -> str:
        return f'TemplateTest(template_id: {self.template_id}, test_id: {self.test_id}, index: {self.index})'
