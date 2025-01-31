from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import event

# Declarative base for all models
class Base(DeclarativeBase):
    pass

# Helper function to register validations before commit
def register_validation_events(model):
    event.listen(model, "before_insert", model.validate_before_commit)
    event.listen(model, "before_update", model.validate_before_commit)