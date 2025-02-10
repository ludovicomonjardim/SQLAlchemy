import pytest
from sqlalchemy.exc import IntegrityError
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


def test_update_actor(actor_repo, session):
    """Testa a atualização do nome de um ator."""
    actor_repo.insert({"name": "Leo"})
    inserted_actor = session.query(Actor).filter_by(name="Leo").first()

    actor_repo.update(where={"name": "Leo"}, with_={"name": "Leonardo DiCaprio"})
    updated_actor = session.query(Actor).filter_by(id=inserted_actor.id).first()
    assert updated_actor.name == "Leonardo DiCaprio"


def test_delete_actor(actor_repo, session):
    """Testa a remoção de um ator."""
    actor_repo.insert({"name": "Brad Pitt"})
    inserted_actor = session.query(Actor).filter_by(name="Brad Pitt").first()
    assert inserted_actor is not None

    actor_repo.delete(where={"name": "Brad Pitt"})
    deleted_actor = session.query(Actor).filter_by(name="Brad Pitt").first()
    assert deleted_actor is None


def test_unique_constraint(actor_repo, session):
    """Testa a restrição de unicidade no nome do ator."""
    actor_repo.insert({"name": "Morgan Freeman"})

    with pytest.raises(IntegrityError):
        actor_repo.insert({"name": "Morgan Freeman"})  # Inserção duplicada deve falhar
