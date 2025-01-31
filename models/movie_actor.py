from models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint

class MovieActor(Base):
    __tablename__ = "movies_actors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    actor_id = Column(Integer, ForeignKey("actors.id"), nullable=False)
    role = Column(String(100))

    __table_args__ = (UniqueConstraint("movie_id", "actor_id"),)
