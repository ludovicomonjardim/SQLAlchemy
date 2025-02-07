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
            print(f"{'Movie ID':<5} {'Actor ID':<5}")
            print("-" * 15)
            for movie_actor in movie_actors:
                print(f"{movie_actor.movie_id:<5} {movie_actor.actor_id:<5}")
        else:
            print("Nenhum(a) ator/atriz encontrado(a) na tabela.")
