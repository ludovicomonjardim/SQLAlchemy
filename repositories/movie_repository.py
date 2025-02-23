"""
repositories/movie_repository.py
Este módulo contém a classe MovieRepository, responsável por interagir com a tabela de filmes no banco de dados.
"""

from repositories.crud_base_repository import CrudBaseRepository
from models.movie import Movie
from models.movie_actor import MovieActor
from models.movie_director import MovieDirector
from models.movie_genre import MovieGenre
from models.classification import Classification
from utils.session import session_manager


class MovieRepository(CrudBaseRepository):
    """
    Classe responsável por operações específicas relacionadas ao modelo Movie no banco de dados.
    Herda métodos genéricos de CrudBaseRepository e implementa funcionalidades específicas, como relatórios e exclusão segura.
    """
    model = Movie

    @staticmethod
    @session_manager(commit=False)  # Apenas leitura, sem commit
    def report(session):
        """
        Exibe todos os filmes cadastrados no banco de dados.
        Mostra título, ano, duração, classificação e status.
        """
        movies = (
            session.query(
                Movie.id,
                Movie.title,
                Movie.year,
                Movie.duration,
                Classification.name.label("classification"),
                Movie.rating,
                Movie.active
            )
            .join(Classification, Classification.id == Movie.classification_id)
            .all()
        )

        if movies:
            print("-" * 120)
            print(f"{'ID':<5} {'Título':<40} {'Ano':<6} {'Duração':<10} {'Classificação':<20} {'Nota':<6} {'Ativo':<8}")
            print("-" * 120)
            for movie in movies:
                duration_display = f"{movie.duration} min" if movie.duration else "N/A"
                rating_display = f"{movie.rating}/10" if movie.rating is not None else "N/A"
                active_display = "Sim" if movie.active else "Não"
                print(
                    f"{movie.id:<5} {movie.title:<40} {movie.year:<6} {duration_display:<10} "
                    f"{movie.classification:<20} {rating_display:<6} {active_display:<8}"
                )
        else:
            print("Nenhum filme encontrado.")

    @session_manager(commit=True)  # Dá commit, pois altera dados
    def delete(self, where, session):
        """
        Exclui um ou mais filmes apenas se não houver sessões de cinema associadas.
        Remove automaticamente associações em `movie_actors`, `movie_directors` e `movie_genres`.
        """
        if not where:
            return {"success": False, "error": "Erro: Nenhum critério de exclusão fornecido."}

        try:
            from models.cinema_session import CinemaSession

            if isinstance(where, dict):
                # 🔹 Excluir um único filme se where for um dicionário
                movie_to_delete = session.query(Movie).filter_by(**where).first()
                if not movie_to_delete:
                    return {"success": False, "error": "Erro: Filme não encontrado."}

                # Verifica se há sessões associadas ao filme
                associated_sessions = session.query(CinemaSession).filter(
                    CinemaSession.movie_id == movie_to_delete.id).count()
                if associated_sessions > 0:
                    return {
                        "success": False,
                        "error": f"Erro: Não é possível excluir '{movie_to_delete.title}', pois está associado a {associated_sessions} sessão(ões) de cinema."
                    }

                # Remove associações antes de excluir o filme
                session.query(MovieActor).filter(MovieActor.movie_id == movie_to_delete.id).delete(
                    synchronize_session=False)
                session.query(MovieDirector).filter(MovieDirector.movie_id == movie_to_delete.id).delete(
                    synchronize_session=False)
                session.query(MovieGenre).filter(MovieGenre.movie_id == movie_to_delete.id).delete(
                    synchronize_session=False)

                result = super().delete(where)
                return result

            elif isinstance(where, list):
                # 🔹 Excluir múltiplos filmes se where for uma lista de expressões
                movies_to_delete = session.query(Movie).filter(*where).all()
                if not movies_to_delete:
                    return {"success": False, "error": "Erro: Nenhum filme encontrado para exclusão."}

                # for movie in movies_to_delete:
                #     associated_sessions = session.query(CinemaSession).filter(
                #         CinemaSession.movie_id == movie.id).count()
                #     if associated_sessions > 0:
                #         return {
                #             "success": False,
                #             "error": f"Erro: Não é possível excluir '{movie.title}', pois está associado a {associated_sessions} sessão(ões) de cinema."
                #         }

                movies_allowed = [movie for movie in movies_to_delete if
                                  session.query(CinemaSession).filter(CinemaSession.movie_id == movie.id).count() == 0]
                if not movies_allowed:
                    return {"success": False, "error": "Nenhum filme pode ser excluído."}

                deleted_count = session.query(Movie).filter(*where).delete(synchronize_session=False)

                if deleted_count == 0:
                    return {"success": False, "error": "Nenhum filme encontrado para exclusão."}

                return {"success": True, "deleted_count": deleted_count}

            else:
                return {"success": False,
                        "error": "Erro: O parâmetro `where` deve ser um dicionário ou uma lista de filtros."}

        except Exception as e:
            return {"success": False, "error": f"Erro ao excluir filme: {e}"}
