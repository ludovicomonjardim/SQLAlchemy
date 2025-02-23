from functools import wraps
from database import Session
from sqlalchemy.exc import (
    DataError, OperationalError, ProgrammingError, DatabaseError,
    SQLAlchemyError, IntegrityError
)
import logging
from utils.logging_config import setup_logger

# Configura o logger
setup_logger()


def _handle_exception(session, exception, func_name, error_message):
    """
    Trata exceções no session_manager, garantindo rollback e log adequado.
    """
    if session.is_active:
        session.rollback()
    logging.warning(f"Session: {error_message} na função '{func_name}': {exception}", exc_info=True)
    return {"success": False, "error": error_message}


def session_manager(commit=True):
    """ Decorador para gerenciar sessões e tratar exceções."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with Session() as session:
                try:
                    result = func(*args, session=session, **kwargs)

                    if commit:
                        session.commit()
                        logging.debug(f"Commit realizado com sucesso na função '{func.__name__}'.")

                    return result if isinstance(result, dict) and "success" in result else {"success": True,
                                                                                            "data": result}

                except DataError as e:
                    return _handle_exception(session, e, func.__name__,
                                             "Erro: Formato de dado inválido ou valor fora do intervalo permitido.")
                except IntegrityError as e:
                    return _handle_exception(session, e, func.__name__,
                                             "Erro: Violação de integridade. Registro duplicado ou dados inválidos.")
                except OperationalError as e:
                    return _handle_exception(session, e, func.__name__,
                                             "Erro operacional: Falha na conexão com o banco de dados.")
                except ProgrammingError as e:
                    return _handle_exception(session, e, func.__name__,
                                             "Erro de programação no banco de dados. Verifique sua consulta SQL ou ORM.")
                except DatabaseError as e:
                    return _handle_exception(session, e, func.__name__,
                                             "Erro interno no banco de dados. Contate o administrador do sistema.")
                except SQLAlchemyError as e:
                    return _handle_exception(session, e, func.__name__,
                                             "SQLAlchemyError. Verifique a lógica da aplicação.")
                except ValueError as e:
                    return _handle_exception(session, e, func.__name__, str(e))
                except Exception as e:
                    return _handle_exception(session, e, func.__name__, f"Erro inesperado: {e}")

        return wrapper

    return decorator
