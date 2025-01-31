from models.base import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates

class Classification(Base):
    __tablename__ = "classifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"Classification: id = {self.id} , name = {self.name}"

    @validates("description")
    def validate_description(self, key, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError("Description must be a non-empty string with a maximum of 50 characters.")
        return value

    @validates("min_age")
    def validate_min_age(self, key, value):
        if not isinstance(value, int) or not (0 <= value <= 18):
            raise ValueError("Minimum age must be an integer between 0 and 18.")
        return value
