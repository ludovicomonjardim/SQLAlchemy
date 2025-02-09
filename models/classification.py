from models.base import Base
from sqlalchemy import Column, String, Integer, CheckConstraint, event
from sqlalchemy.orm import validates, Session

class Classification(Base):
    __tablename__ = "classifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(15), unique=True, nullable=False)  # Limitando tamanho no banco
    description = Column(String(50), nullable=False)  # Adicionando campo ausente
    min_age = Column(Integer, nullable=False)  # Adicionando campo ausente

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0 AND LENGTH(name) <= 15", name="check_classification_name"),
        CheckConstraint("LENGTH(description) > 0 AND LENGTH(description) <= 50", name="check_classification_description"),
        CheckConstraint("min_age BETWEEN 0 AND 18", name="check_min_age_range"),
    )

    def __repr__(self):
        return f"<Classification(id={self.id}, name='{self.name}', min_age={self.min_age})>"

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip() or len(value) > 15:
            raise ValueError("Classification name must be a non-empty string with a maximum of 15 characters.")
        return value.strip()

    @validates("description")
    def validate_description(self, key, value):
        if not isinstance(value, str) or not value.strip() or len(value) > 50:
            raise ValueError("Description must be a non-empty string with a maximum of 50 characters.")
        return value.strip()

    @validates("min_age")
    def validate_min_age(self, key, value):
        if not isinstance(value, int) or not (0 <= value <= 18):
            raise ValueError("Minimum age must be an integer between 0 and 18.")
        return value

# Validação antes do commit
@event.listens_for(Session, "before_flush")
def validate_classification_before_commit(session, flush_context, instances):
    for instance in session.new | session.dirty:  # Valida inserções e atualizações
        if isinstance(instance, Classification):
            if not isinstance(instance.name, str) or not instance.name.strip() or len(instance.name) > 15:
                raise ValueError("Classification name must be a non-empty string with a maximum of 15 characters.")
            if not isinstance(instance.description, str) or not instance.description.strip() or len(instance.description) > 50:
                raise ValueError("Description must be a non-empty string with a maximum of 50 characters.")
            if not isinstance(instance.min_age, int) or not (0 <= instance.min_age <= 18):
                raise ValueError("Minimum age must be an integer between 0 and 18.")
