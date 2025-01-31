from models.base import Base
from sqlalchemy import Column, Integer, String, Date, Time, DECIMAL, ForeignKey
from sqlalchemy.orm import validates

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    room = Column(String(10), nullable=False)
    capacity = Column(Integer, nullable=False)
    price = Column(DECIMAL(6, 2), nullable=False)

    @validates("capacity")
    def validate_capacity(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Capacity must be an integer greater than zero.")
        return value
