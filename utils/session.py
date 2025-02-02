import logging
from functools import wraps
from database import Session

# Logging configuration
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Decorator to manage sessions
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
                logging.error(f"Session error: {e}", exc_info=True)
                raise
    return wrapper
