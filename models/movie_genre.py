from models.base import Base
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, event, PrimaryKeyConstraint
from sqlalchemy.orm import Session

class MovieGenre(Base):
    __tablename__ = "movie_genre"  # Nome padronizado no singular

    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("movie_id", "genre_id", name="uq_movie_genre"),
        PrimaryKeyConstraint("movie_id", "genre_id")
    )

    def __repr__(self):
        return f"<MovieGenre(id={self.id}, movie_id={self.movie_id}, genre_id={self.genre_id})>"

# Validação antes do commit
@event.listens_for(Session, "before_flush")
def validate_movie_genre_before_commit(session, flush_context, instances):
    for instance in session.new | session.dirty:  # Valida inserções e atualizações
        if isinstance(instance, MovieGenre):
            if not isinstance(instance.movie_id, int) or not isinstance(instance.genre_id, int):
                raise ValueError("Both movie_id and genre_id must be valid integers.")
