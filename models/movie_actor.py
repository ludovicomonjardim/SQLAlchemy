from models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, CheckConstraint, event, PrimaryKeyConstraint
from sqlalchemy.orm import validates, Session

class MovieActor(Base):
    __tablename__ = "movie_actor"  # Nome padronizado no singular

    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    actor_id = Column(Integer, ForeignKey("actors.id"), nullable=False)
    role = Column(String(100), nullable=True)

    __table_args__ = (
        UniqueConstraint("movie_id", "actor_id", name="uq_movie_actor"),
        PrimaryKeyConstraint("movie_id", "actor_id"),
        CheckConstraint("LENGTH(role) > 0 OR role IS NULL", name="check_movie_actor_role"),
    )

    def __repr__(self):
        return f"<MovieActor(id={self.id}, movie_id={self.movie_id}, actor_id={self.actor_id}, role='{self.role}')>"

    @validates("role")
    def validate_role(self, key, value):
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError("Role must be a non-empty string if provided.")
        return value.strip() if value else None

# Validação antes do commit
@event.listens_for(Session, "before_flush")
def validate_movie_actor_before_commit(session, flush_context, instances):
    for instance in session.new | session.dirty:  # Valida inserções e atualizações
        if isinstance(instance, MovieActor):
            if instance.role is not None and (not isinstance(instance.role, str) or not instance.role.strip()):
                raise ValueError("Role must be a non-empty string if provided.")
