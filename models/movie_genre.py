from models.base import Base
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

class MovieGenre(Base):
    __tablename__ = "movies_genres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)

    __table_args__ = (UniqueConstraint("movie_id", "genre_id"),)
