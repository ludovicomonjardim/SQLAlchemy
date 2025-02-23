import pytest
import time
from sqlalchemy import inspect, text
from database import engine, get_session
from models.base import Base
from sqlalchemy.exc import OperationalError
from database import engine


@pytest.fixture(scope="function")
def session():
    """Cria uma sessão para os testes e garante limpeza ao final."""
    session = get_session()
    yield session
    session.rollback()
    session.close()


def test_database_connection():
    """Verifica se a conexão com o banco pode ser estabelecida, considerando tempo de inicialização no Docker."""
    retries = 5
    for attempt in range(retries):
        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                assert result.fetchone()[0] == 1
                return  # Sai do teste caso funcione
        except OperationalError:
            if attempt < retries - 1:
                time.sleep(2)  # Aguarda 2 segundos antes de tentar novamente
            else:
                pytest.fail("Não foi possível conectar ao banco de dados.")


def test_tables_creation():
    """Verifica se todas as tabelas são criadas corretamente."""
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())  # 🔹 Lista todas as tabelas no banco
    expected_tables = {
        "actors", "directors", "genres", "classifications", "movies",
        "movie_actor", "movie_director", "movie_genre", "cinema_sessions", "tickets"
    }
    print(f"Tabelas encontradas no banco de dados: {tables}")  # 🔹 DEBUG

    assert expected_tables.issubset(tables), f"Faltam tabelas: {expected_tables - tables}"

def test_session_rollback(session):
    """Verifica se o rollback está funcionando corretamente."""
    from models.actor import Actor
    session.add(Actor(name="Teste Actor"))
    session.rollback()
    actor = session.query(Actor).filter_by(name="Teste Actor").first()
    assert actor is None, "Rollback falhou: o ator ainda está no banco."


def test_session_isolation(session):
    """Verifica se a sessão é isolada para cada teste."""
    from models.actor import Actor

    # 🔹 Remover qualquer ator com o mesmo nome antes de testar
    session.query(Actor).filter_by(name="Isolated Actor").delete()
    session.commit()

    # 🔹 Inserir o novo registro
    session.add(Actor(name="Isolated Actor"))
    session.commit()

    # 🔹 Criar uma nova sessão e verificar se o registro existe
    new_session = get_session()
    actor = new_session.query(Actor).filter_by(name="Isolated Actor").first()
    assert actor is not None, "A sessão não manteve os dados corretamente."
    new_session.close()

