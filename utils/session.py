import logging
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
                logging.error(f"Erro na sessão: {e}", exc_info=True)
                raise
    return wrapper
