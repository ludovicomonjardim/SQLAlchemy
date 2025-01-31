from models.base import Base
from sqlalchemy import Column, String, Integer, event
from sqlalchemy.orm import validates, Session

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"Genre: id = {self.id} , name = {self.name}"

    @validates("name")
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError("Genre name must be a non-empty string with a maximum of 50 characters.")
        return value

# Evento para validar antes do commit
@event.listens_for(Session, "before_flush")
def validate_genre_before_commit(session, flush_context, instances):
    for instance in session.new | session.dirty:  # Valida tanto inserções quanto atualizações
        if isinstance(instance, Genre):
            if not isinstance(instance.name, str) or not instance.name.strip() or len(instance.name) > 50:
                raise ValueError("Genre name must be a non-empty string with a maximum of 50 characters.")