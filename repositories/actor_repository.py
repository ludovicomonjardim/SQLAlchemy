from repositories.crud_base_repository import CrudBaseRepository
from repositories.movie_actor_repository import MovieActorRepository
from models.actor import Actor
from utils.session import session_manager

class ActorRepository(CrudBaseRepository):
    model = Actor  # Definição do modelo correto

    @staticmethod
    @session_manager
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

    @session_manager
    def delete(self, where, session):
        """
        Exclui um ator e também remove suas associações na tabela movie_actors.

        :param where: Dicionário com as condições para exclusão do ator.
        :param session: Sessão do banco (gerenciada automaticamente).
        :return: Mensagem indicando sucesso ou erro.
        """
        # Buscar o ator antes de excluir
        actor_to_delete = session.query(Actor).filter_by(**where).first()

        if not actor_to_delete:
            return "Erro: Ator não encontrado."

        # Remover todas as associações do ator na tabela movie_actors usando MovieActorRepository
        movie_actor_repo = MovieActorRepository()
        result_associations = movie_actor_repo.delete({"id": actor_to_delete.id}, ignore_if_not_found=True)

        # Verifica se houve erro ao excluir as associações
        if isinstance(result_associations, str):  # Se `delete` retornou um erro
            return result_associations  # Retorna a mensagem de erro

        # Agora podemos remover o ator com segurança
        result = super().delete(where)

        if isinstance(result, str):  # Se `session_manager` retornou um erro
            return result

        return f"Ator '{actor_to_delete.name}' e suas associações foram removidos com sucesso."
