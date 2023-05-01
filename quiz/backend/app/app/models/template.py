from sqlalchemy import Integer, String, Column

from app.database.base_class import Base


# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-models
# no need for __tablename__ because of declarative style (app.database.base_class)
class Template(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'Template(id: {self.id}, name: {self.name})'
