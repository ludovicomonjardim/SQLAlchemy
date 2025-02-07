import logging
from functools import wraps
from database import Session
from sqlalchemy.exc import DataError, OperationalError, ProgrammingError, DatabaseError, SQLAlchemyError

# Configuração de logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Decorador para gerenciar sessões e tratar exceções
def session_manager(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Session() as session:
            try:
                result = func(*args, session=session, **kwargs)  # Executa a função com a sessão injetada
                session.commit()  # Faz commit apenas se tudo der certo
                return result  # Retorna o resultado esperado

            except DataError:
                session.rollback()
                return "Erro: Formato de dado inválido ou valor fora do intervalo permitido."

            except OperationalError:
                session.rollback()
                return "Erro operacional: Falha na conexão com o banco de dados."

            except ProgrammingError:
                session.rollback()
                return "Erro de programação: Verifique a estrutura da consulta ou do banco de dados."

            except DatabaseError:
                session.rollback()
                return "Erro grave no banco de dados. Tente novamente mais tarde."

            except SQLAlchemyError:
                session.rollback()
                return "Erro inesperado ao acessar o banco de dados."

            except Exception as e:
                session.rollback()
                logging.error(f"Session error: {e}", exc_info=True)
                return f"Erro inesperado: {e}"

    return wrapper
