from models.base import Base
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, event
from sqlalchemy.orm import Session

class MovieDirector(Base):
    __tablename__ = "movie_directors"  # Nome padronizado no singular

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("movie_id", "director_id", name="uq_movie_director"),
    )

    def __repr__(self):
        return f"<MovieDirector(id={self.id}, movie_id={self.movie_id}, director_id={self.director_id})>"

# Validação antes do commit
@event.listens_for(Session, "before_flush")
def validate_movie_director_before_commit(session, flush_context, instances):
    for instance in session.new | session.dirty:  # Valida inserções e atualizações
        if isinstance(instance, MovieDirector):
            if not isinstance(instance.movie_id, int) or not isinstance(instance.director_id, int):
                raise ValueError("Both movie_id and director_id must be valid integers.")
