import pytest
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import DATABASE_URL
from database import engine, Session
from models.base import Base


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
    engine = create_engine(DATABASE_URL)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()

    # Criar as tabelas no banco de dados de testes
    Base.metadata.create_all(engine)

    yield session  # Retorna a sessão para os testes

    # Fechar a sessão após o teste
    session.close()
    Base.metadata.drop_all(engine)  # Remove as tabelas ao final do teste


@pytest.fixture(scope="function")
def db_session():
    """Cria um banco de testes e garante que cada teste tenha um ambiente limpo."""
    Base.metadata.create_all(engine)  # Cria as tabelas
    session = Session()
    yield session  # Executa o teste
    session.rollback()  # Desfaz todas as operações
    session.close()
