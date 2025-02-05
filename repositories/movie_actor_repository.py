from repositories.crud_base_repository import CrudBaseRepository
from models.movie_actor import MovieActor
from utils.session import session_manager

class MovieActorRepository(CrudBaseRepository):
    model = MovieActor

    @staticmethod
    @session_manager
    def print_all(session):
        # Exibe todos os(as) atores/atrizes cadastrados(as) no banco de dados.
        movie_actors = session.query(MovieActor).all()
        if movie_actors:
            print()
            print("-" * 30)
            print(f"{'ID':<5} {'Nome':<20}")
            print("-" * 30)
            for movie_actor in movie_actors:
                print(f"{movie_actor.id:<5} {movie_actor.name:<20}")
        else:
            print("Nenhum(a) ator/atriz encontrado(a) na tabela.")