from models.base import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates

class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"Director: id = {self.id} , name = {self.name}"


    @validates("name")
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or len(value) > 100:
            raise ValueError("Director name must be a non-empty string with a maximum of 100 characters.")
        return value
