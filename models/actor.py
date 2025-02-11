from models.base import Base
from sqlalchemy import Column, String, Integer, CheckConstraint, UniqueConstraint, event
from sqlalchemy.orm import validates, Session

class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0 AND LENGTH(name) <= 100", name="check_actor_name"),
        UniqueConstraint("name", name="uq_actor_name")  # 🔹 Garante unicidade
    )

    def __repr__(self):
        return f"<Actor(id={self.id}, name='{self.name}')>"

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip() or len(value) > 100:
            raise ValueError("Actor name must be a non-empty string with a maximum of 100 characters.")
        return value.strip()

# Validação antes do commit
@event.listens_for(Session, "before_flush")
def validate_actor_before_commit(session, flush_context, instances):
    for instance in session.new | session.dirty:  # Valida tanto novas inserções quanto atualizações
        if isinstance(instance, Actor):
            if not isinstance(instance.name, str) or not instance.name.strip() or len(instance.name) > 100:
                raise ValueError("Actor name must be a non-empty string with a maximum of 100 characters.")
