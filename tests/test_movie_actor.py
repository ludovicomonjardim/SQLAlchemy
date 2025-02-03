import pytest
from sqlalchemy.exc import IntegrityError
from models.movie_actor import MovieActor
from models.movie import Movie
from models.actor import Actor
from models.movie_genre import MovieGenre
from models.movie_director import MovieDirector
from models.cinema_session import CinemaSession
from models.ticket import Ticket
from database import initialize_database, get_session


@pytest.fixture(scope="function")
def session():
    """Cria uma sessão temporária para os testes."""
    initialize_database()
    session = get_session()
    yield session
    session.rollback()
    session.close()


def test_unique_constraint(session):
    """Testa a restrição de unicidade movie_id + actor_id."""

    # 🔥 **Certifica que todas as tabelas relacionadas são limpas antes do teste**
    session.query(MovieActor).delete(synchronize_session=False)
    session.query(MovieGenre).delete(synchronize_session=False)
    session.query(MovieDirector).delete(synchronize_session=False)
    session.query(Ticket).delete(synchronize_session=False)
    session.query(CinemaSession).delete(synchronize_session=False)
    session.query(Movie).delete(synchronize_session=False)
    session.query(Actor).delete(synchronize_session=False)
    session.commit()  # 🔥 **Garante que os dados antigos foram removidos**

    actor = Actor(name="Tom Cruise")
    movie = Movie(title="Mission Impossible", year=1996, duration=110, classification_id=4, rating=7)
    session.add(actor)
    session.add(movie)
    session.commit()

    movie_actor1 = MovieActor(movie_id=movie.id, actor_id=actor.id, role="Agente Secreto")
    session.add(movie_actor1)
    session.commit()

    # Tentativa de inserir duplicado deve falhar
    movie_actor2 = MovieActor(movie_id=movie.id, actor_id=actor.id, role="Agente Secreto")
    session.add(movie_actor2)

    # 🔥 Captura explicitamente a exceção esperada ao tentar flush()
    with pytest.raises(IntegrityError):
        session.flush()  # 🚀 **Garante que o erro ocorra antes do commit**

    session.rollback()  # 🔥 **Evita que a transação corrompa o restante dos testes**
