import pytest
from repositories.actor_repository import ActorRepository
from models.actor import Actor
from models.movie_actor import MovieActor
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
    """Testa a inserção de um ator sem duplicidade."""
    session.query(MovieActor).delete(synchronize_session=False)
    session.query(Actor).delete(synchronize_session=False)
    session.commit()

    assert actor_repo.insert({"name": "Leonardo DiCaprio"}) == 1  # Corrigido
    assert actor_repo.insert({"name": "Leonardo DiCaprio"}) == 0  # Deve falhar ao inserir duplicado

def test_update_actor(actor_repo, session):
    """Testa a atualização do nome de um ator sem causar duplicidade."""
    session.query(MovieActor).delete(synchronize_session=False)
    session.query(Actor).delete(synchronize_session=False)
    session.commit()

    actor_repo.insert({"name": "Leo"})
    assert actor_repo.update(where={"name": "Leo"}, with_={"name": "Leonardo DiCaprio"}) == 1
    assert actor_repo.update(where={"name": "Leonardo DiCaprio"}, with_={"name": "Leo"}) == 1  # Voltar ao original

def test_delete_actor(actor_repo, session):
    """Testa a remoção de um ator, garantindo que todas referências sejam apagadas antes."""
    session.query(MovieActor).delete(synchronize_session=False)
    session.query(Actor).delete(synchronize_session=False)
    session.commit()

    actor_repo.insert({"name": "Brad Pitt"})
    inserted_actor = session.query(Actor).filter_by(name="Brad Pitt").first()
    assert inserted_actor is not None

    session.query(MovieActor).filter_by(actor_id=inserted_actor.id).delete(synchronize_session=False)
    session.commit()

    assert actor_repo.delete(where={"name": "Brad Pitt"}) == 1
    assert actor_repo.delete(where={"name": "Brad Pitt"}) == 0  # Não pode deletar de novo!
