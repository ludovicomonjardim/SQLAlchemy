from models.base import Base
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

class MovieDirector(Base):
    __tablename__ = "movies_directors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=False)

    __table_args__ = (UniqueConstraint("movie_id", "director_id"),)
