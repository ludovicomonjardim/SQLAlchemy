from models.base import Base
from sqlalchemy import Column, String, Integer, CheckConstraint, event
from sqlalchemy.orm import validates, Session

class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)  # Definindo limite no schema

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0 AND LENGTH(name) <= 100", name="check_director_name"),
    )

    def __repr__(self):
        return f"<Director(id={self.id}, name='{self.name}')>"

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip() or len(value) > 100:
            raise ValueError("Director name must be a non-empty string with a maximum of 100 characters.")
        return value.strip()  # Remove espaços extras

# Validação antes do commit
@event.listens_for(Session, "before_flush")
def validate_director_before_commit(session, flush_context, instances):
    for instance in session.new | session.dirty:  # Valida inserções e atualizações
        if isinstance(instance, Director):
            if not isinstance(instance.name, str) or not instance.name.strip() or len(instance.name) > 100:
                raise ValueError("Director name must be a non-empty string with a maximum of 100 characters.")
