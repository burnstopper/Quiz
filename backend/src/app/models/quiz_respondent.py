from sqlalchemy import Integer, Column

from app.database.base_class import Base


# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-models
# no need for __tablename__ because of declarative style (app.database.base_class)
class QuizRespondent(Base):
    respondent_id = Column(Integer, primary_key=True, nullable=False)
    quiz_id = Column(Integer, primary_key=True, nullable=False)

    def __repr__(self) -> str:
        return f'(QuizRespondent)(respondent_id: {self.respondent_id}, quiz_id: {self.quiz_id})'
