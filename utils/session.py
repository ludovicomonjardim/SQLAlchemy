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
                        logging.info(f"Commit realizado com sucesso na função '{func.__name__}'.")

                    # 🔹 Evita aninhamento extra: se já for um dicionário com "success", retorna diretamente
                    if isinstance(result, dict) and "success" in result:
                        return result

                    return {"success": True, "data": result}  # Apenas encapsula se necessário

                except DataError as e:
                    session.rollback()
                    logging.error(f"Erro de formato de dado inválido na função '{func.__name__}': {e}", exc_info=True)
                    return {"success": False, "error": "Erro: Formato de dado inválido ou valor fora do intervalo permitido."}

                except IntegrityError as e:
                    session.rollback()
                    logging.error(f"Erro de integridade: {e}", exc_info=True)
                    return {"success": False, "error": "Erro: Violação de integridade. Registro duplicado ou dados inválidos."}

                except OperationalError as e:
                    session.rollback()
                    logging.error(f"Erro operacional: {e}", exc_info=True)
                    return {"success": False, "error": "Erro operacional: Falha na conexão com o banco de dados."}

                except Exception as e:
                    session.rollback()
                    logging.error(f"Erro inesperado '{func.__name__}': {e}", exc_info=True)
                    return {"success": False, "error": f"Erro inesperado: {e}"}

        return wrapper
    return decorator

