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
    """Testa a atualização do nome de um ator garantindo que os nomes não existam previamente."""

    # Remove qualquer ator com os nomes envolvidos no teste para evitar conflitos
    session.query(Actor).filter(Actor.name.in_(["Ludo", "Ludovico Monjardim"])).delete(synchronize_session=False)
    session.commit()

    # Insere um ator com um nome único
    actor_repo.insert({"name": "Ludo"})
    inserted_actor = session.query(Actor).filter_by(name="Ludo").first()

    # Atualiza o nome do ator
    actor_repo.update(where={"name": "Ludo"}, with_={"name": "Ludovico Monjardim"})
    session.expire_all()
    updated_actor = session.query(Actor).filter_by(id=inserted_actor.id).first()

    # Valida se o nome foi atualizado corretamente
    assert updated_actor.name == "Ludovico Monjardim"


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

    # Remove o ator se já existir para garantir um teste limpo
    session.query(Actor).filter(Actor.name == "Morgan Freeman").delete(synchronize_session=False)
    session.commit()


    # Insere o ator pela primeira vez (deve ter sucesso)
    result1 = actor_repo.insert({"name": "Morgan Freeman"})
    assert result1["success"] is True, f"Falha na primeira inserção: {result1['error']}"

    # Tenta inserir o mesmo nome novamente (deve falhar)
    result2 = actor_repo.insert({"name": "Morgan Freeman"})

    assert result2["success"] is False, "A inserção duplicada deveria falhar, mas foi bem-sucedida."
    assert "Violação de integridade" in result2["error"], f"Erro inesperado: {result2['error']}"

