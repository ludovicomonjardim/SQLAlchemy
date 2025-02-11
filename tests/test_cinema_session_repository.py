import pytest
from sqlalchemy.exc import IntegrityError
from repositories.cinema_session_repository import CinemaSessionRepository
from models.cinema_session import CinemaSession
from models.movie import Movie
from database import initialize_database, get_session
from datetime import datetime, date, time, UTC


@pytest.fixture(scope="function")
def session():
    """Cria uma sessão temporária para os testes."""
    initialize_database()
    session = get_session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def cinema_session_repo(session):
    """Instancia o repositório de sessões de cinema para os testes."""
    return CinemaSessionRepository()


@pytest.fixture(scope="function")
def movie(session):
    """Cria um filme antes dos testes para garantir um `movie_id` válido."""
    new_movie = Movie(
        title="Matrix",
        year=1999,
        duration=136,
        classification_id=1,  # 🔹 Supondo que a classificação ID 1 exista
        rating=9,
        active=True
    )
    session.add(new_movie)
    session.commit()
    return new_movie


@pytest.fixture(scope="function")
def cinema_session(session, movie):
    """Cria uma sessão de cinema fictícia antes dos testes."""
    new_session = CinemaSession(
        movie_id=movie.id,  # 🔹 Agora usamos um ID de filme válido
        date=date.today(),
        time=time(20, 0),
        room="Sala 1",
        capacity=100,
        price=30.00
    )
    session.add(new_session)
    session.commit()
    return new_session


def test_insert_cinema_session(cinema_session_repo, session, movie):
    """Testa a inserção de uma sessão de cinema."""
    session_data = {
        "movie_id": movie.id,
        "date": date.today(),
        "time": time(19, 30),
        "room": "Sala 2",
        "capacity": 80,
        "price": 25.00
    }
    cinema_session_repo.insert(session_data)

    inserted_session = session.query(CinemaSession).filter_by(movie_id=movie.id, room="Sala 2").first()
    assert inserted_session is not None
    assert inserted_session.capacity == 80
    assert inserted_session.price == 25.00


def test_insert_cinema_session_invalid_movie(cinema_session_repo, session):
    """Testa a inserção de uma sessão de cinema com um `movie_id` inválido."""
    session_data = {
        "movie_id": 99999,  # 🔹 Filme inexistente
        "date": date.today(),
        "time": time(19, 30),
        "room": "Sala 3",
        "capacity": 50,
        "price": 20.00
    }

    result = cinema_session_repo.insert(session_data)
    assert result["success"] is False
    assert "Erro: Violação de integridade" in result["error"]


def test_insert_duplicate_cinema_session(cinema_session_repo, session, movie):
    """Testa a inserção duplicada de uma sessão de cinema no mesmo horário e sala."""
    session_data = {
        "movie_id": movie.id,
        "date": date.today(),
        "time": time(19, 30),
        "room": "Sala 2",
        "capacity": 80,
        "price": 25.00
    }

    cinema_session_repo.insert(session_data)
    result = cinema_session_repo.insert(session_data)

    assert result["success"] is False
    assert "Erro: Violação de integridade" in result["error"]


def test_delete_cinema_session(cinema_session_repo, session, cinema_session):
    """Testa a remoção de uma sessão de cinema sem ingressos associados."""
    result = cinema_session_repo.delete({"id": cinema_session.id})
    assert result["success"] is True, f"Falha ao excluir sessão: {result['error']}"

    deleted_session = session.query(CinemaSession).filter_by(id=cinema_session.id).first()
    assert deleted_session is None

def test_delete_cinema_session_with_tickets(cinema_session_repo, session, cinema_session):
    """Testa a remoção de uma sessão de cinema com ingressos vinculados."""
    from models.ticket import Ticket

    # Criando um ingresso para a sessão
    session.add(Ticket(cinema_session_id=cinema_session.id, customer="Cliente 1"))
    session.commit()

    result = cinema_session_repo.delete({"id": cinema_session.id})

    assert result["success"] is False
    assert "Não é possível excluir a sessão" in result["error"]
    assert "ingresso(s) vendidos" in result["error"]  # 🔹 Garante que o erro menciona ingressos vendidos