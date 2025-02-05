from repositories.crud_base_repository import CrudBaseRepository
from models.cinema_session import CinemaSession
from utils.session import session_manager

class CinemaSessionRepository(CrudBaseRepository):
    model = CinemaSession

    @staticmethod
    @session_manager
    def print_all(session):
        # Exibe todos as seções cadastradas no banco de dados.
        cinema_sessions = session.query(CinemaSession).all()
        if cinema_sessions:
            print()
            print("-" * 30)
            print(f"{'ID':<5} {'Nome':<20}")
            print("-" * 30)
            for cinema_session in cinema_sessions:
                print(f"{cinema_session.id:<5} {cinema_session.name:<20}")
        else:
            print("Nenhuma seção encontrada na tabela.")