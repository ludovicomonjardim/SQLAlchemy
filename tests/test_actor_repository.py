import pytest
import logging
import time
from models.actor import Actor
from repositories.actor_repository import ActorRepository
from utils.logging_config import setup_logger

# Configura o logger
setup_logger(complete=False)

logging.basicConfig(level=logging.DEBUG)

@pytest.fixture(scope="function")
def actor_repo(session):
    """Retorna uma instância do repositório de atores usando a sessão de teste."""
    return ActorRepository()


def test_insert_actor(session, actor_repo):
    """Testa a inserção de um ator válido no banco de dados."""

    # Tenta inserir um ator válido
    result = actor_repo.insert({"name": "Leonardo DiCaprio"})
    # Verifica se a inserção foi bem-sucedida
    assert result["success"] is True

    # Obtém o ID do ator inserido
    inserted_actor_id = result["data"]
    assert isinstance(inserted_actor_id, int)  # Garante que o retorno é um ID válido

    # Busca o ator no banco usando o ID retornado
    actor = session.get(Actor, inserted_actor_id)  # SQLAlchemy 2.0 (mais eficiente)

    # Confirma que o ator foi inserido corretamente
    assert actor is not None
    assert actor.name == "Leonardo DiCaprio"


def test_delete_actor_with_dependencies(session, actor_repo):
    """Testa a exclusão de um ator que está relacionado a um filme na tabela movie_actor."""
    from models.classification import Classification
    from models.movie import Movie
    from models.movie_actor import MovieActor

    # Criar uma classificação válida antes do filme
    classification = Classification(id=1, name="PG-13", description="Apenas maiores de 13 anos", min_age=13)
    session.add(classification)
    session.commit()

    # Criar um ator e um filme
    actor = Actor(name="Johnny Depp")
    movie = Movie(title="Pirates of the Caribbean", year=2003, classification_id=1)
    session.add(actor)
    session.add(movie)
    session.commit()

    # Criar a relação entre ator e filme
    movie_actor = MovieActor(movie_id=movie.id, actor_id=actor.id)
    session.add(movie_actor)
    session.commit()

    # Garante que a relação foi criada corretamente
    assert session.query(MovieActor).filter_by(actor_id=actor.id).count() == 1

    # Exclui o ator e verifica se a relação em movie_actor foi removida
    result = actor_repo.delete({"id": actor.id})
    # Remove explicitamente o ator da sessão para evitar erros ao acessá-lo
    session.expunge(actor)
    # Consulta segura, pois o objeto não está mais na sessão
    remaining_actor = session.query(Actor).filter_by(id=actor.id).first()

    assert result["success"] is True
    assert session.query(MovieActor).filter_by(actor_id=actor.id).count() == 0
    assert remaining_actor is None


def test_select_actor(session, actor_repo):
    """Testa a consulta de um ator existente."""
    actor = Actor(name="Meryl Streep")
    session.add(actor)
    session.commit()

    result = actor_repo.select(where={"name": "Meryl Streep"})
    assert result["success"] is True
    assert len(result["data"]) == 1
    assert result["data"][0].name == "Meryl Streep"


def test_update_actor(session, actor_repo):
    """Testa a atualização do nome de um ator."""
    actor = Actor(name="Robert Downey Jr.")
    session.add(actor)
    session.commit()

    result = actor_repo.update({"name": "Robert Downey Jr."}, {"name": "RDJ"})
    assert result["success"] is True
    updated_actor = session.query(Actor).filter_by(name="RDJ").first()
    assert updated_actor is not None
    assert updated_actor.name == "RDJ"


def test_delete_actor(session, actor_repo):
    """Testa a exclusão de um ator."""
    actor = Actor(name="Tom Hanks")
    session.add(actor)
    session.commit()

    result = actor_repo.delete({"name": "Tom Hanks"})
    assert result["success"] is True
    deleted_actor = session.query(Actor).filter_by(name="Tom Hanks").first()
    assert deleted_actor is None


def test_insert_duplicate_actor(session, actor_repo):
    """Testa erro ao tentar inserir um ator com nome duplicado."""
    session.add(Actor(name="Morgan Freeman"))
    session.commit()

    result = actor_repo.insert({"name": "Morgan Freeman"})
    assert result["success"] is False
    assert "Violação de integridade" in result["error"]


def test_insert_invalid_actor(session, actor_repo):
    """Testa erro ao tentar inserir um ator com nome vazio."""
    result = actor_repo.insert({"name": ""})
    assert result["success"] is False
    assert "Actor name must be a non-empty string" in result["error"]


def test_insert_multiple_actors(session, actor_repo):
    """Testa a inserção de múltiplos atores simultaneamente."""
    actors = [{"name": "Actor 1"}, {"name": "Actor 2"}, {"name": "Actor 3"}]
    result = actor_repo.insert(actors)
    assert result["success"] is True
    assert len(result["data"]) == 3


def test_delete_non_existent_actor(session, actor_repo):
    """Testa a exclusão de um ator inexistente."""
    result = actor_repo.delete({"name": "Fake Actor"})
    assert result["success"] is False
    assert "Nenhum registro encontrado" in result["error"]


def test_select_actor_by_id(session, actor_repo):
    """Testa a consulta de um ator pelo ID."""
    actor = Actor(name="Harrison Ford")
    session.add(actor)
    session.commit()

    result = actor_repo.select(where={"id": actor.id})
    assert result["success"] is True
    assert len(result["data"]) == 1
    assert result["data"][0].name == "Harrison Ford"


def test_bulk_insert_and_delete(session, actor_repo):
    """Testa inserção e exclusão em lote de atores."""
    actors = [{"name": "Batch 1"}, {"name": "Batch 2"}, {"name": "Batch 3"}]
    insert_result = actor_repo.insert(actors)
    assert insert_result["success"] is True

    delete_result = actor_repo.delete({})
    assert delete_result["success"] is True

def test_bulk_insert_performance(session, actor_repo):
    start = time.time()
    actors = [{"name": f"Ator {i}"} for i in range(1000)]
    result = actor_repo.insert(actors)
    duration = time.time() - start

    assert result["success"]
    assert duration < 2  # Exemplo: garantir que 1000 inserções ocorram em menos de 2s.