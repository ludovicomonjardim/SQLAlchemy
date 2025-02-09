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
        Exclui um ator e suas associações com filmes.
        - Recebe um dicionário 'where' com critérios para localizar o ator.
        - Remove as associações do ator com filmes antes de excluí-lo.
        - Retorna um dicionário indicando sucesso ou falha da operação.
        """

        # Busca o ator com base nos critérios fornecidos.
        actor_to_delete = session.query(Actor).filter_by(**where).first()
        if not actor_to_delete:
            # Retorna erro se o ator não for encontrado.
            return {"success": False, "error": "Erro: Ator não encontrado."}

        # Instancia o repositório para gerenciar associações entre filmes e atores.
        movie_actor_repo = MovieActorRepository()
        # Remove as associações do ator.
        result_associations = movie_actor_repo.delete({"id": actor_to_delete.id}, ignore_if_not_found=True)
        if not result_associations["success"]:
            # Retorna o erro ocorrido durante a remoção das associações.
            return result_associations

        # Chama o delete da classe pai (CrudBaseRepository) para remover o ator.
        result = super().delete(where)
        if not result["success"]:
            # Retorna o erro ocorrido durante a exclusão do ator.
            return result

        # Retorna mensagem de sucesso.
        return {"success": True, "message": f"Ator '{actor_to_delete.name}' removido com sucesso."}