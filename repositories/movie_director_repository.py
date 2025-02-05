from repositories.crud_base_repository import CrudBaseRepository
from models.movie_director import MovieDirector
from utils.session import session_manager

class MovieDirectorRepository(CrudBaseRepository):
    model = MovieDirector

    @staticmethod
    @session_manager
    def print_all(session):
        # Exibe todos os(as) atores/atrizes cadastrados(as) no banco de dados.
        movie_directors = session.query(MovieDirector).all()
        if movie_directors:
            print()
            print("-" * 30)
            print(f"{'ID':<5} {'Nome':<20}")
            print("-" * 30)
            for movie_director in movie_directors:
                print(f"{movie_director.id:<5} {movie_director.name:<20}")
        else:
            print("Nenhum(a) diretor(a) encontrado(a) na tabela.")