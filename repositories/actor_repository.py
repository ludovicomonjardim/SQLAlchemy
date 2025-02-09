from repositories.crud_base_repository import CrudBaseRepository
from repositories.movie_actor_repository import MovieActorRepository
from models.actor import Actor
from utils.session import session_manager

class ActorRepository(CrudBaseRepository):
    model = Actor

    @staticmethod
    @session_manager(commit=False)  # Não dá commit, pois não altera dados
    def report(session):
        """Exibe todos os atores cadastrados."""
        actors = session.query(Actor).all()
        if actors:
            print("-" * 51)
            print(f"{'ID':<5} {'Nome':<45}")
            print("-" * 51)
            for actor in actors:
                print(f"{actor.id:<5} {actor.name:<45}")
        else:
            print("Nenhum ator encontrado na tabela.")

    @session_manager(commit=True)  # Dá commit, pois altera dados
    def delete(self, where, session):
        """Exclui um ator e suas associações."""
        actor_to_delete = session.query(Actor).filter_by(**where).first()

        if not actor_to_delete:
            return {"success": False, "error": "Erro: Ator não encontrado."}

        movie_actor_repo = MovieActorRepository()
        result_associations = movie_actor_repo.delete({"id": actor_to_delete.id}, ignore_if_not_found=True)

        if not result_associations["success"]:
            return result_associations

        result = super().delete(where)

        if not result["success"]:
            return result

        return {"success": True, "message": f"Ator '{actor_to_delete.name}' removido com sucesso."}
