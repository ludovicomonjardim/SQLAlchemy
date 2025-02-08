import logging
from functools import wraps
from database import Session
from sqlalchemy.exc import DataError, OperationalError, ProgrammingError, DatabaseError, SQLAlchemyError

import logging
from utils.logging_config import setup_logger

# Configura o logger
setup_logger()

# Decorador para gerenciar sessões e tratar exceções
def session_manager(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Session() as session:
            try:
                result = func(*args, session=session, **kwargs)  # Executa a função com a sessão injetada
                session.commit()  # Faz commit apenas se tudo der certo
                logging.info(f"Commit realizado com sucesso na função '{func.__name__}'.")
                return result  # Retorna o resultado esperado

            except DataError as e:
                session.rollback()
                logging.error(f"Erro de formato de dado inválido na função '{func.__name__}': {e}", exc_info=True)
                return "Erro: Formato de dado inválido ou valor fora do intervalo permitido."

            except OperationalError as e:
                session.rollback()
                logging.error(f"Erro operacional: Falha na conexão com o banco de dados. '{func.__name__}': {e}", exc_info=True)
                return "Erro operacional: Falha na conexão com o banco de dados."

            except ProgrammingError as e:
                session.rollback()
                logging.error(f"Erro de programação: Verifique a estrutura da consulta ou do banco de dados. '{func.__name__}': {e}", exc_info=True)
                return "Erro de programação: Verifique a estrutura da consulta ou do banco de dados."

            except DatabaseError as e:
                session.rollback()
                logging.error(f"Erro grave no banco de dados. Tente novamente mais tarde. '{func.__name__}': {e}", exc_info=True)
                return "Erro grave no banco de dados. Tente novamente mais tarde."

            except SQLAlchemyError as e:
                session.rollback()
                logging.error(f"Erro inesperado ao acessar o banco de dados. '{func.__name__}': {e}", exc_info=True)
                return "Erro inesperado ao acessar o banco de dados."

            except Exception as e:
                session.rollback()
                logging.error(f"Erro inesperado '{func.__name__}': {e}", exc_info=True)
                return f"Erro inesperado: {e}"

    return wrapper
