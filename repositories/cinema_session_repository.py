"""
repositories/cinema_session_repository.py
Este módulo contém a classe CinemaSessionRepository, responsável por interagir com a tabela de sessões de cinema no banco de dados.
"""

from repositories.crud_base_repository import CrudBaseRepository
from repositories.ticket_repository import TicketRepository
from models.cinema_session import CinemaSession
from models.movie import Movie
from utils.session import session_manager


class CinemaSessionRepository(CrudBaseRepository):
    """
    Classe responsável por operações específicas relacionadas ao modelo CinemaSession no banco de dados.
    Herda métodos genéricos de CrudBaseRepository e implementa funcionalidades específicas, como relatórios e exclusão.
    """
    model = CinemaSession

    @staticmethod
    @session_manager(commit=False)  # Apenas leitura, sem commit
    def report(session):
        """
        Exibe todas as sessões de cinema cadastradas no banco de dados.
        Agora mostra o título do filme, além da data, hora, sala, capacidade e preço formatados corretamente.
        """
        sessions = (
            session.query(
                CinemaSession.id,
                Movie.title,  # 🔹 Obtém o título do filme
                CinemaSession.date,
                CinemaSession.time,
                CinemaSession.room,
                CinemaSession.capacity,
                CinemaSession.price
            )
            .join(Movie, Movie.id == CinemaSession.movie_id)  # 🔹 Faz o JOIN com a tabela de filmes
            .all()
        )

        if sessions:
            print("-" * 110)
            print(f"{'ID':<5} {'Filme':<30} {'Data':<12} {'Hora':<8} {'Sala':<10} {'Capacidade':<10} {'Preço':<10}")
            print("-" * 110)
            for session in sessions:
                formatted_date = session.date.strftime("%d/%m/%Y") if session.date else "N/A"
                formatted_time = session.time.strftime("%H:%M") if session.time else "N/A"
                print(
                    f"{session.id:<5} {session.title:<30} {formatted_date:<12} {formatted_time:<8} "
                    f"{session.room:<10} {session.capacity:<10} {session.price:<10.2f}"
                )
        else:
            print("Nenhuma sessão de cinema encontrada.")

    @session_manager(commit=True)  # Dá commit, pois altera dados
    def delete(self, where, session):
        """
        Exclui um ou mais diretores e suas associações com filmes.
        - Remove todas as dependências antes de excluir o diretor.
        - Usa `delete_with_dependencies()` para garantir exclusão segura.
        """

        return super().delete_with_dependencies(
            where=where,
            related_models=[(TicketRepository.model, "cinema_session_id")]
        )