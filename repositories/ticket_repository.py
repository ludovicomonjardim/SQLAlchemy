from repositories.crud_base_repository import CrudBaseRepository
from models.ticket import Ticket
from utils.session import session_manager

class TicketRepository(CrudBaseRepository):
    model = Ticket

    @staticmethod
    @session_manager
    def print_all(session):
        # Exibe todos os gêneros cadastrados no banco de dados.
        tickets = session.query(Ticket).all()
        if tickets:
            print()
            print("-" * 30)
            print(f"{'ID':<5} {'Nome':<20}")
            print("-" * 30)
            for ticket in tickets:
                print(f"{ticket.id:<5} {ticket.name:<20}")
        else:
            print("Nenhum ingresso encontrado na tabela.")