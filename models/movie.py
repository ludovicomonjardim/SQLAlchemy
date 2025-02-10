from models.base import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, CheckConstraint, UniqueConstraint, event
from sqlalchemy.orm import validates, relationship, Session

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    year = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=True)  # Pode ser nulo
    synopsis = Column(Text, nullable=True)  # Pode ser nulo
    classification_id = Column(Integer, ForeignKey("classifications.id"), nullable=False)
    rating = Column(Integer, nullable=True)  # Pode ser nulo
    active = Column(Boolean, default=True, nullable=False)

    classification = relationship("Classification")

    __table_args__ = (
        CheckConstraint("LENGTH(title) > 0 AND LENGTH(title) <= 200", name="check_movie_title"),
        CheckConstraint("year BETWEEN 1888 AND 2100", name="check_movie_year"),
        CheckConstraint("duration IS NULL OR duration > 0", name="check_movie_duration"),
        CheckConstraint("rating IS NULL OR (rating BETWEEN 0 AND 10)", name="check_movie_rating"),
        UniqueConstraint("title", "year", "duration", name="uq_movie_title_year_duration"),
    )

    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.title}', year={self.year}, duration={self.duration}, active={self.active})>"

    @validates("title")
    def validate_title(self, key, value):
        if not isinstance(value, str) or not value.strip() or len(value) > 200:
            raise ValueError("Title must be a non-empty string with a maximum of 200 characters.")
        return value.strip()

    @validates("year")
    def validate_year(self, key, value):
        if not isinstance(value, int) or not (1888 <= value <= 2100):
            raise ValueError("Year must be an integer between 1888 and 2100.")
        return value

    @validates("duration")
    def validate_duration(self, key, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError("Duration must be a positive integer.")
        return value

    @validates("rating")
    def validate_rating(self, key, value):
        if value is not None and (not isinstance(value, int) or not (0 <= value <= 10)):
            raise ValueError("Rating must be an integer between 0 and 10.")
        return value

# Validação antes do commit
@event.listens_for(Session, "before_flush")
def validate_movie_before_commit(session, flush_context, instances):
    for instance in session.new | session.dirty:  # Valida inserções e atualizações
        if isinstance(instance, Movie):
            if not isinstance(instance.title, str) or not instance.title.strip() or len(instance.title) > 200:
                raise ValueError("Title must be a non-empty string with a maximum of 200 characters.")
            if not isinstance(instance.year, int) or not (1888 <= instance.year <= 2100):
                raise ValueError("Year must be an integer between 1888 and 2100.")
            if instance.duration is not None and (not isinstance(instance.duration, int) or instance.duration <= 0):
                raise ValueError("Duration must be a positive integer.")
            if instance.rating is not None and (not isinstance(instance.rating, int) or not (0 <= instance.rating <= 10)):
                raise ValueError("Rating must be an integer between 0 and 10.")
