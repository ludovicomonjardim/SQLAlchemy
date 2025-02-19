import pytest
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import engine, Session
from models.base import Base
from database import DATABASE_URL, engine, initialize_database, get_session


def wait_for_database():
    """Aguarda o banco de dados estar disponível antes de rodar os testes."""
    engine = create_engine(DATABASE_URL)
    retries = 5
    for attempt in range(retries):
        try:
            with engine.connect():
                return  # Sai da função caso consiga conectar
        except Exception:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise RuntimeError("Banco de dados não está acessível.")

# Chama essa função antes de criar a sessão para testes
wait_for_database()


@pytest.fixture(scope="function")
def session():
    """Cria uma sessão do SQLAlchemy para os testes."""

    # 🔹 Inicializa o banco de dados corretamente antes de cada teste
    initialize_database()

    # Criar a sessão para os testes
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()

    yield session  # Retorna a sessão para os testes

    # Fecha a sessão após o teste
    session.close()
