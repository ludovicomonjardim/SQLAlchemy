from repositories.crud_base_repository import CrudBaseRepository
from models.actor import Actor
from utils.session import session_manager

class ActorRepository(CrudBaseRepository):
    model = Actor

    @staticmethod
    @session_manager
    def print_all(session):
        # Exibe todos os gêneros cadastrados no banco de dados.
        actors = session.query(Actor).all()
        if actors:
            print()
            print("-" * 30)
            print(f"{'Id':<5} {'Nome':<20}")
            print("-" * 30)
            for actor in actors:
                print(f"{actor.id:<5} {actor.name:<20}")
        else:
            print("Nenhum ator encontrado na tabela.")