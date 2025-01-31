from models.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, CheckConstraint, event
from sqlalchemy.orm import validates, Session
from datetime import datetime, UTC

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    customer = Column(String(100), nullable=False)  # Definição explícita como obrigatório
    purchase_date = Column(DateTime, default=func.now(), nullable=False)  # Não pode ser nulo

    __table_args__ = (
        CheckConstraint("LENGTH(customer) > 0 AND LENGTH(customer) <= 100", name="check_ticket_customer"),
    )

    def __repr__(self):
        return f"<Ticket(id={self.id}, session_id={self.session_id}, customer='{self.customer}', purchase_date={self.purchase_date})>"

    @validates("customer")
    def validate_customer(self, key, value):
        if not isinstance(value, str) or not value.strip() or len(value) > 100:
            raise ValueError("Customer name must be a non-empty string with a maximum of 100 characters.")
        return value.strip()

    @validates("purchase_date")
    def validate_purchase_date(self, key, value):
        """Ensures that purchase_date is not in the future."""
        if value and value > datetime.now(UTC):
            raise ValueError("Purchase date cannot be in the future.")
        return value

# Validação antes do commit
@event.listens_for(Session, "before_flush")
def validate_ticket_before_commit(session, flush_context, instances):
    for instance in session.new | session.dirty:  # Valida inserções e atualizações
        if isinstance(instance, Ticket):
            if not isinstance(instance.customer, str) or not instance.customer.strip() or len(instance.customer) > 100:
                raise ValueError("Customer name must be a non-empty string with a maximum of 100 characters.")
            if instance.purchase_date and instance.purchase_date > datetime.now(UTC):
                raise ValueError("Purchase date cannot be in the future.")
