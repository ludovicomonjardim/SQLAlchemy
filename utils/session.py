import logging
from functools import wraps
from database import Session

# Configuração do logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

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
                logging.error(f"Erro na sessão: {e}", exc_info=True)
                raise
    return wrapper
