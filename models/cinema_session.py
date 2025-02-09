from models.base import Base
from sqlalchemy import Column, Integer, String, Date, Time, DECIMAL, ForeignKey, CheckConstraint, event
from sqlalchemy.orm import validates, Session
from datetime import datetime, date, time

from models.base import Base
from sqlalchemy import Column, Integer, String, Date, Time, DECIMAL, ForeignKey, CheckConstraint, UniqueConstraint, event
from sqlalchemy.orm import validates, Session
from datetime import date, time

class CinemaSession(Base):
    __tablename__ = "cinema_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    room = Column(String(10), nullable=False)
    capacity = Column(Integer, nullable=False)
    price = Column(DECIMAL(6, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("capacity > 0", name="check_session_capacity"),
        CheckConstraint("price >= 0", name="check_session_price"),
        CheckConstraint("LENGTH(room) > 0", name="check_session_room"),
        UniqueConstraint("movie_id", "date", "time", "room", name="uq_cinema_session"),  # 🔹 Impede duplicação
    )

    def __repr__(self):
        return f"<CinemaSession(id={self.id}, movie_id={self.movie_id}, date={self.date}, time={self.time}, room='{self.room}', capacity={self.capacity}, price={self.price})>"

    @validates("capacity")
    def validate_capacity(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Capacity must be an integer greater than zero.")
        return value

    @validates("price")
    def validate_price(self, key, value):
        if value is None or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number.")
        return value

    @validates("room")
    def validate_room(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Room must be a non-empty string.")
        return value.strip()

    @validates("date")
    def validate_date(self, key, value):
        if not isinstance(value, date):
            raise ValueError("Date must be a valid date object.")
        return value

    @validates("time")
    def validate_time(self, key, value):
        if not isinstance(value, time):
            raise ValueError("Time must be a valid time object.")
        return value


# Validação antes do commit
@event.listens_for(Session, "before_flush")
def validate_session_before_commit(session, flush_context, instances):
    for instance in session.new | session.dirty:  # Valida inserções e atualizações
        if isinstance(instance, CinemaSession):
            if not isinstance(instance.capacity, int) or instance.capacity <= 0:
                raise ValueError("Capacity must be an integer greater than zero.")
            if instance.price is None or not isinstance(instance.price, (int, float)) or instance.price < 0:
                raise ValueError("Price must be a non-negative number.")
            if not isinstance(instance.room, str) or not instance.room.strip():
                raise ValueError("Room must be a non-empty string.")
            if not isinstance(instance.date, date):
                raise ValueError("Date must be a valid date object.")
            if not isinstance(instance.time, time):
                raise ValueError("Time must be a valid time object.")
