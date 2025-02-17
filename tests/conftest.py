import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import DATABASE_URL  # A URL do banco de dados
from database import engine, Session
from models.base import Base

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
