from models.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import validates
from datetime import datetime, UTC

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    customer = Column(String(100))
    purchase_date = Column(DateTime, default=func.now())

    @validates("purchase_date")
    def validate_purchase_date(self, key, value):
        """Ensures that purchase_date is not in the future."""
        if value and value > datetime.now(UTC):
            raise ValueError("Purchase date cannot be in the future.")
        return value