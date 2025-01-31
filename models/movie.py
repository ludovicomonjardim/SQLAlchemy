from models.base import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    year = Column(Integer, nullable=False)
    duration = Column(Integer)
    synopsis = Column(Text)
    classification_id = Column(Integer, ForeignKey("classifications.id"), nullable=False)
    rating = Column(Integer)
    active = Column(Boolean, default=True)

    classification = relationship("Classification")

    def __repr__(self):
        return f"Movie: Title = {self.title}, Year = {self.year}', Duration = {self.duration} Active = {self.active})"

    @validates("title")
    def validate_title(self, key, value):
        if not value or not isinstance(value, str) or len(value) > 200:
            raise ValueError("Title must be a non-empty string with a maximum of 200 characters.")
        return value

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