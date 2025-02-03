import pytest
from repositories.movie_repository import MovieRepository
from database import initialize_database, get_session
from models.movie import Movie
from models.movie_genre import MovieGenre
from models.movie_director import MovieDirector
from models.movie_genre import MovieGenre
from models.movie_director import MovieDirector
from models.movie_actor import MovieActor
from models.cinema_session import CinemaSession
from models.ticket import Ticket

@pytest.fixture(scope="function")
def session():
    """Cria uma sessão temporária para os testes."""
    initialize_database()  # Garante que o BD esteja inicializado
    session = get_session()
    yield session
    session.rollback()  # Limpa as alterações após o teste
    session.close()


@pytest.fixture(scope="function")
def movie_repo(session):
    """Instancia o repositório de filmes para os testes."""
    return MovieRepository()


def test_insert_movie(movie_repo, session):
    """Testa a inserção de um filme."""
    movie_data = {"title": "The Matrix", "year": 1999, "duration": 136, "classification_id": 4, "rating": 9}
    movie_repo.insert(movie_data)

    inserted_movie = session.query(Movie).filter_by(title="The Matrix").first()
    assert inserted_movie is not None
    assert inserted_movie.title == "The Matrix"
    assert inserted_movie.year == 1999


def test_get_movie_by_id(movie_repo, session):
    """Testa a recuperação de um filme pelo ID."""
    movie_data = {"title": "Inception", "year": 2010, "duration": 148, "classification_id": 4, "rating": 9}
    movie_repo.insert(movie_data)

    inserted_movie = session.query(Movie).filter_by(title="Inception").first()

    # ✅ Correção: Usando `get_by_field` em vez de `get_by_id`
    fetched_movie = movie_repo.get_by_field(where={"id": inserted_movie.id})

    assert fetched_movie is not None
    assert fetched_movie[0]["title"] == "Inception"  # A resposta agora é uma lista de dicionários


def test_update_movie(movie_repo, session):
    """Testa a atualização de um filme."""
    movie_data = {"title": "Interstellar", "year": 2014, "duration": 169, "classification_id": 4, "rating": 10}
    movie_repo.insert(movie_data)

    inserted_movie = session.query(Movie).filter_by(title="Interstellar").first()

    movie_repo.update(where={"title": "Interstellar"}, with_={"year": 2015})

    session.commit()  # 🔥 Adicionando commit para garantir que a atualização foi aplicada no BD

    updated_movie = session.query(Movie).filter_by(id=inserted_movie.id).first()
    session.refresh(updated_movie)  # 🔥 Força a atualização dos dados mais recentes do BD

    assert updated_movie.year == 2015


from models.movie_genre import MovieGenre
from models.movie_director import MovieDirector
from models.movie_actor import MovieActor
from models.cinema_session import CinemaSession

def test_delete_movie(movie_repo, session):
    """Testa a remoção de um filme sem violação de chave estrangeira."""
    movie_data = {"title": "Pulp Fiction", "year": 1994, "duration": 154, "classification_id": 5, "rating": 8}
    movie_repo.insert(movie_data)

    inserted_movie = session.query(Movie).filter_by(title="Pulp Fiction").first()
    assert inserted_movie is not None

    # ✅ Remove todas as referências antes de excluir o filme
    session.query(Ticket).filter(Ticket.cinema_session_id.in_(
        session.query(CinemaSession.id).filter_by(movie_id=inserted_movie.id)
    )).delete(synchronize_session=False)

    session.query(CinemaSession).filter_by(movie_id=inserted_movie.id).delete(synchronize_session=False)
    session.query(MovieGenre).filter_by(movie_id=inserted_movie.id).delete(synchronize_session=False)
    session.query(MovieDirector).filter_by(movie_id=inserted_movie.id).delete(synchronize_session=False)
    session.query(MovieActor).filter_by(movie_id=inserted_movie.id).delete(synchronize_session=False)

    session.commit()  # Confirma a remoção das relações antes de excluir o filme

    movie_repo.delete(where={"title": "Pulp Fiction"})

    deleted_movie = session.query(Movie).filter_by(title="Pulp Fiction").first()
    assert deleted_movie is None