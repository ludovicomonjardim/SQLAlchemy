"""
repositories.actor_repository
Este módulo contém a classe ActorRepository, responsável por interagir com a tabela de atores no banco de dados.
"""

from repositories.crud_base_repository import CrudBaseRepository
from repositories.movie_actor_repository import MovieActorRepository
from models.actor import Actor
from utils.session import session_manager


class ActorRepository(CrudBaseRepository):
    """
    Classe responsável por operações específicas relacionadas ao modelo Actor no banco de dados.
    Herda métodos genéricos de CrudBaseRepository e implementa funcionalidades específicas, como relatórios e exclusão.
    """
    model = Actor

    @staticmethod
    @session_manager(commit=False)  # Não dá commit, pois não altera dados
    def report(session):
        """
        Exibe todos os atores cadastrados no banco de dados.
        - A função recebe uma sessão do banco de dados como argumento.
        - Consulta todos os registros da tabela 'Actor'.
        - Se houver atores, exibe-os em um formato tabular.
        - Caso contrário, informa que nenhum ator foi encontrado.
        """
        # Realiza uma consulta para obter todos os atores.
        actors = session.query(Actor).all()
        if actors:
            print("-" * 51)
            print(f"{'ID':<5} {'Nome':<45}")
            print("-" * 51)
            # Itera sobre cada ator retornado.
            for actor in actors:
                print(f"{actor.id:<5} {actor.name:<45}")
        else:
            # Mensagem caso a tabela esteja vazia.
            print("Nenhum ator encontrado na tabela.")

    @session_manager(commit=True)  # Dá commit, pois altera dados
    def delete(self, where, session):
        """
        Exclui um ou mais atores e suas associações com filmes.
        - Recebe `where`, que pode ser um dicionário (exclusão única) ou uma lista de filtros (exclusão múltipla).
        - Remove as associações antes de excluir o ator.
        - Retorna um dicionário indicando sucesso ou falha da operação.
        """

        if not where:
            return {"success": False, "error": "Erro: Nenhum critério de exclusão fornecido."}

        try:
            # Se `where` for um dicionário, usa `filter_by`
            if isinstance(where, dict):
                actor_to_delete = session.query(Actor).filter_by(**where).first()
                if not actor_to_delete:
                    return {"success": False, "error": "Erro: Ator não encontrado."}

                # Exclui associações do ator antes de removê-lo
                movie_actor_repo = MovieActorRepository()
                result_associations = movie_actor_repo.delete({"id": actor_to_delete.id}, ignore_if_not_found=True)
                if not result_associations["success"]:
                    return result_associations

                result = super().delete(where)
                if not result["success"]:
                    return result

                return {"success": True, "message": f"Ator '{actor_to_delete.name}' removido com sucesso."}

            # Se `where` for uma lista, usa `filter`
            elif isinstance(where, list):
                query = session.query(Actor).filter(*where)
                deleted_count = query.delete(synchronize_session=False)

                if deleted_count == 0:
                    return {"success": False, "error": "Nenhum ator encontrado para exclusão."}

                return {"success": True, "deleted_count": deleted_count}

            else:
                return {"success": False,
                        "error": "Erro: O parâmetro `where` deve ser um dicionário ou uma lista de filtros."}

        except Exception as e:
            return {"success": False, "error": f"Erro ao excluir registros: {e}"}
