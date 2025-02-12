import pytest
from sqlalchemy.exc import IntegrityError
from repositories.ticket_repository import TicketRepository
from models.ticket import Ticket
from models.cinema_session import CinemaSession
from models.movie import Movie
from database import initialize_database, get_session
from datetime import datetime, UTC


@pytest.fixture(scope="function")
def session():
    """Cria uma sessão temporária para os testes."""
    initialize_database()
    session = get_session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def ticket_repo(session):
    """Instancia o repositório de ingressos para os testes."""
    return TicketRepository()


@pytest.fixture(scope="function")
def movie(session):
    """Cria um filme fictício antes dos testes."""
    new_movie = Movie(title="Filme Teste", year=2025, duration=120, classification_id=1, rating=8, active=True)
    session.add(new_movie)
    session.commit()
    return new_movie


@pytest.fixture(scope="function")
def cinema_session(session, movie):
    """Cria uma sessão de cinema fictícia antes dos testes, associada a um filme existente."""
    new_session = CinemaSession(
        movie_id=movie.id,  # 🔹 Agora garantimos que o filme existe
        date=datetime.now(UTC).date(),
        time=datetime.now(UTC).time(),
        room="Sala 1",
        capacity=100,
        price=25.00
    )
    session.add(new_session)
    session.commit()
    return new_session


def test_insert_ticket(ticket_repo, session, cinema_session):
    """Testa a inserção de um ingresso."""
    ticket = {"cinema_session_id": cinema_session.id, "customer": "John Doe"}
    ticket_repo.insert(ticket)

    inserted_ticket = session.query(Ticket).filter_by(cinema_session_id=cinema_session.id).first()
    assert inserted_ticket is not None
    assert inserted_ticket.customer == "John Doe"


def test_insert_ticket_invalid_session(ticket_repo, session):
    """Testa a inserção de um ingresso com um `cinema_session_id` inválido."""
    ticket = {"cinema_session_id": 99999, "customer": "Jane Doe"}  # 🔹 Sessão de cinema inexistente

    result = ticket_repo.insert(ticket)
    assert result["success"] is False
    assert "Erro: A sessão de cinema ID 99999 não existe." in result["error"]


def test_insert_multi_ticket(ticket_repo, session, cinema_session):
    """Testa a inserção múltipla de ingressos."""

    # 🔹 Garante que a sessão de cinema não tem ingressos antes do teste
    session.query(Ticket).filter_by(cinema_session_id=cinema_session.id).delete(synchronize_session=False)
    session.commit()

    tickets_data = [
        {"cinema_session_id": cinema_session.id, "customer": "Alice Johnson"},
        {"cinema_session_id": cinema_session.id, "customer": "Bob Smith"},
        {"cinema_session_id": cinema_session.id, "customer": "Charlie Brown"},
    ]

    result = ticket_repo.insert(tickets_data)

    assert result["success"] is True, f"Falha na inserção múltipla: {result['error']}"

    inserted_tickets = session.query(Ticket).filter(Ticket.cinema_session_id == cinema_session.id).all()
    assert len(inserted_tickets) == 3, f"Esperado 3 ingressos, mas encontrou {len(inserted_tickets)}"



def test_delete_ticket(ticket_repo, session, cinema_session):
    """Testa a remoção de um ingresso."""
    ticket_repo.insert({"cinema_session_id": cinema_session.id, "customer": "Quentin Tarantino"})
    inserted_ticket = session.query(Ticket).filter_by(cinema_session_id=cinema_session.id).first()
    assert inserted_ticket is not None

    ticket_repo.delete(where={"id": inserted_ticket.id})
    deleted_ticket = session.query(Ticket).filter_by(id=inserted_ticket.id).first()
    assert deleted_ticket is None


def test_unique_constraint_not_required(ticket_repo, session, cinema_session):
    """Testa se é possível vender múltiplos ingressos para a mesma sessão e cliente."""
    ticket_repo.insert({"cinema_session_id": cinema_session.id, "customer": "Chris Evans"})
    result = ticket_repo.insert({"cinema_session_id": cinema_session.id, "customer": "Chris Evans"})

    # 🔹 Aqui não há restrição de unicidade, pois múltiplos ingressos podem ser comprados pelo mesmo cliente
    assert result["success"] is True, f"Erro inesperado: {result['error']}"
