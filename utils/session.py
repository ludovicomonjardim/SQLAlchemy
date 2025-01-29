from functools import wraps
from database import Session

# Decorador para gerenciar sessões
def session_manager(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Session() as session:
            try:
                result = func(*args, session=session, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                print(f"Erro: {e}")
                raise
    return wrapper
