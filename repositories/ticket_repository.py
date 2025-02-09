"""
repositories/ticket_repository.py
Este módulo contém a classe TicketRepository, responsável por interagir com a tabela de ingressos no banco de dados.
"""

from repositories.crud_base_repository import CrudBaseRepository
from models.ticket import Ticket
from models.cinema_session import CinemaSession
from utils.session import session_manager
from datetime import datetime, UTC


class TicketRepository(CrudBaseRepository):
    """
    Classe responsável por operações específicas relacionadas ao modelo Ticket no banco de dados.
    Herda métodos genéricos de CrudBaseRepository e implementa funcionalidades específicas, como relatórios.
    """
    model = Ticket

    @staticmethod
    @session_manager(commit=False)  # Apenas leitura, sem commit
    def report(session):
        """
        Exibe todos os ingressos cadastrados no banco de dados.
        Agora mostra o título do filme da sessão, além do nome do cliente e data da compra.
        """
        tickets = (
            session.query(
                Ticket.id,
                CinemaSession.id.label("session_id"),
                Ticket.customer,
                Ticket.purchase_date
            )
            .join(CinemaSession, CinemaSession.id == Ticket.cinema_session_id)
            .all()
        )

        if tickets:
            print("-" * 100)
            print(f"{'ID':<5} {'Sessão':<8} {'Cliente':<30} {'Data da Compra':<20}")
            print("-" * 100)
            for ticket in tickets:
                formatted_date = ticket.purchase_date.strftime("%d/%m/%Y %H:%M") if ticket.purchase_date else "N/A"
                print(f"{ticket.id:<5} {ticket.session_id:<8} {ticket.customer:<30} {formatted_date:<20}")
        else:
            print("Nenhum ingresso encontrado.")

    @session_manager(commit=True)  # Dá commit, pois altera dados
    def insert(self, data, session):
        """
        Insere um novo ingresso no banco de dados.
        - Verifica se a sessão de cinema associada existe antes de inserir.
        """
        session_exists = session.query(CinemaSession).filter_by(id=data["cinema_session_id"]).first()
        if not session_exists:
            return {"success": False, "error": f"Erro: A sessão de cinema ID {data['cinema_session_id']} não existe."}

        return super().insert(data)
