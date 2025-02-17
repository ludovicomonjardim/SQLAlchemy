import pytest

from repositories.actor_repository import ActorRepository
from models.actor import Actor
from database import initialize_database, get_session


@pytest.fixture(scope="function")
def session():
    """Cria uma sessão temporária para os testes."""
    initialize_database()
    session = get_session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def actor_repo(session):
    """Instancia o repositório de atores para os testes."""
    return ActorRepository()


def test_insert_actor(actor_repo, session):
    """Testa a inserção de um ator."""
    actor = {"name": "Leonardo DiCaprio"}
    actor_repo.insert(actor)

    inserted_actor = session.query(Actor).filter_by(name="Leonardo DiCaprio").first()
    assert inserted_actor is not None
    assert inserted_actor.name == "Leonardo DiCaprio"
