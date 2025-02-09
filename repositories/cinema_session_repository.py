"""
repositories/cinema_session_repository.py
Este módulo contém a classe CinemaSessionRepository, responsável por interagir com a tabela de sessões de cinema no banco de dados.
"""

from repositories.crud_base_repository import CrudBaseRepository
from models.cinema_session import CinemaSession
from models.movie import Movie
from utils.session import session_manager
from datetime import date, time


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
        Exclui uma ou mais sessões de cinema apenas se não houver ingressos associados.
        - `where` pode ser um dicionário (exclusão única) ou uma lista de filtros (exclusão múltipla).
        - Retorna um dicionário indicando sucesso ou falha da operação.
        """
        if not where:
            return {"success": False, "error": "Erro: Nenhum critério de exclusão fornecido."}

        try:
            from models.ticket import Ticket

            if isinstance(where, dict):
                # 🔹 Excluir um único registro se where for um dicionário
                session_to_delete = session.query(CinemaSession).filter_by(**where).first()
                if not session_to_delete:
                    return {"success": False, "error": "Erro: Sessão de cinema não encontrada."}

                # Verifica se há ingressos associados à sessão
                associated_tickets = session.query(Ticket).filter(
                    Ticket.cinema_session_id == session_to_delete.id).count()
                if associated_tickets > 0:
                    return {
                        "success": False,
                        "error": f"Erro: Não é possível excluir a sessão {session_to_delete.id}, pois possui {associated_tickets} ingresso(s) vendidos."
                    }

                # Prossegue com a exclusão
                result = super().delete(where)
                if not result["success"]:
                    return result

                return {"success": True, "message": f"Sessão {session_to_delete.id} removida com sucesso."}

            elif isinstance(where, list):
                # 🔹 Excluir múltiplos registros se where for uma lista de expressões
                sessions_to_delete = session.query(CinemaSession).filter(*where).all()
                if not sessions_to_delete:
                    return {"success": False, "error": "Erro: Nenhuma sessão encontrada para exclusão."}

                for session_obj in sessions_to_delete:
                    associated_tickets = session.query(Ticket).filter(
                        Ticket.cinema_session_id == session_obj.id).count()
                    if associated_tickets > 0:
                        return {
                            "success": False,
                            "error": f"Erro: Não é possível excluir a sessão {session_obj.id}, pois possui {associated_tickets} ingresso(s) vendidos."
                        }

                deleted_count = session.query(CinemaSession).filter(*where).delete(synchronize_session=False)

                if deleted_count == 0:
                    return {"success": False, "error": "Nenhuma sessão encontrada para exclusão."}

                return {"success": True, "deleted_count": deleted_count}

            else:
                return {"success": False,
                        "error": "Erro: O parâmetro `where` deve ser um dicionário ou uma lista de filtros."}

        except Exception as e:
            return {"success": False, "error": f"Erro ao excluir sessão de cinema: {e}"}


