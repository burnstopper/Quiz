from sqlalchemy import Integer, String, Column

from app.database.base_class import Base


# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-models
# no need for __tablename__ because of declarative style (app.database.base_class)
class Quiz(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    template_id = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    invite_link = Column(String, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f'(Quiz)(id: {self.id}, template_id: {self.template_id}, name: {self.name})'
