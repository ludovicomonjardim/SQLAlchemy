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
        - Remove todas as dependências antes de excluir o ator.
        - Usa `delete_with_dependencies()` para garantir exclusão segura.
        """

        return super().delete_with_dependencies(
            where=where,
            related_models=[(MovieActorRepository.model, "actor_id")]
        )
