from repositories.crud_base_repository import CrudBaseRepository
from models.movie_genre import MovieGenre
from utils.session import session_manager

class MovieGenreRepository(CrudBaseRepository):
    model = MovieGenre

    @staticmethod
    @session_manager
    def print_all(session):
        # Exibe todos os(as) atores/atrizes cadastrados(as) no banco de dados.
        movie_genres = session.query(MovieGenre).all()
        if movie_genres:
            print()
            print("-" * 30)
            print(f"{'Movie ID':<5} {'Genre ID':<5}")
            print("-" * 15)
            for movie_genre in movie_genres:
                print(f"{movie_genre.movie_id:<5} {movie_genre.actor_id:<5}")
        else:
            print("Nenhum(a) ator/atriz encontrado(a) na tabela.")