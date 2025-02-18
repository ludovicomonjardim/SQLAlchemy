from functools import wraps
from database import Session
from sqlalchemy.exc import DataError, OperationalError, ProgrammingError, DatabaseError, SQLAlchemyError, IntegrityError

import logging
from utils.logging_config import setup_logger

# Configura o logger
setup_logger()

# Decorador para gerenciar sessões e tratar exceções
def session_manager(commit=True):  # Parâmetro para definir se deve dar commit
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with Session() as session:
                try:
                    result = func(*args, session=session, **kwargs)  # Executa a função

                    if commit:
                        session.commit()
                        logging.debug(f"Commit realizado com sucesso na função '{func.__name__}'.")

                    # Evita aninhamento extra: se já for um dicionário com "success", retorna diretamente
                    if isinstance(result, dict) and "success" in result:
                        return result

                    return {"success": True, "data": result}  # Apenas encapsula se necessário

                except DataError as e:
                    if session.is_active:
                        session.rollback()
                    logging.warning(f"Session: Erro de formato de dado inválido na função '{func.__name__}': {e}", exc_info=True)
                    return {"success": False, "error": "Erro: Formato de dado inválido ou valor fora do intervalo permitido."}

                except IntegrityError as e:
                    if session.is_active:
                        session.rollback()
                    logging.warning(f"Session: Erro de integridade: {e}", exc_info=True)
                    return {"success": False, "error": "Erro: Violação de integridade. Registro duplicado ou dados inválidos."}

                except OperationalError as e:
                    if session.is_active:
                        session.rollback()
                    logging.warning(f"Session: Erro operacional: {e}", exc_info=True)
                    return {"success": False, "error": "Erro operacional: Falha na conexão com o banco de dados."}

                except ProgrammingError as e:
                    if session.is_active:
                        session.rollback()
                    logging.warning(f"Session: Erro de programação no banco de dados na função '{func.__name__}': {e}", exc_info=True)
                    return {"success": False, "error": "Erro de programação no banco de dados. Verifique sua consulta SQL ou ORM."}

                except DatabaseError as e:
                    if session.is_active:
                        session.rollback()
                    logging.warning(f"Session: Erro interno no banco de dados na função '{func.__name__}': {e}", exc_info=True)
                    return {"success": False, "error": "Erro interno no banco de dados. Contate o administrador do sistema."}

                except SQLAlchemyError as e:
                    if session.is_active:
                        session.rollback()
                    logging.warning(f"Session: Erro geral do SQLAlchemy na função '{func.__name__}': {e}", exc_info=True)
                    return {"success": False, "error": "SQLAlchemyError. Verifique a lógica da aplicação."}

                except ValueError as e:
                    if session.is_active:
                        session.rollback()
                    logging.warning(f"Session: Erro de validação: '{func.__name__}': {e}")  # Alterado para warning
                    return {"success": False, "error": str(e)}

                except Exception as e:
                    if session.is_active:
                        session.rollback()
                    logging.warning(f"Session: Erro inesperado '{func.__name__}': {e}", exc_info=True)
                    return {"success": False, "error": f"Erro inesperado: {e}"}

        return wrapper
    return decorator

