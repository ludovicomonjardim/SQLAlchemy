"""
repositories/director_repository.py
Este módulo contém a classe DirectorRepository, responsável por interagir com a tabela de diretores no banco de dados.
"""

from repositories.crud_base_repository import CrudBaseRepository
from repositories.movie_director_repository import MovieDirectorRepository
from models.director import Director
from utils.session import session_manager


class DirectorRepository(CrudBaseRepository):
    """
    Classe responsável por operações específicas relacionadas ao modelo Director no banco de dados.
    Herda métodos genéricos de CrudBaseRepository e implementa funcionalidades específicas, como relatórios e exclusão.
    """
    model = Director

    @staticmethod
    @session_manager(commit=False)  # Não dá commit, pois apenas faz leitura
    def report(session):
        """
        Exibe todos os diretores cadastrados no banco de dados.
        - A função recebe uma sessão do banco de dados como argumento.
        - Consulta todos os registros da tabela 'Director'.
        - Se houver diretores, exibe-os em um formato tabular.
        - Caso contrário, informa que nenhum diretor foi encontrado.
        """
        directors = session.query(Director).all()
        if directors:
            print("-" * 51)
            print(f"{'ID':<5} {'Nome':<45}")
            print("-" * 51)
            for director in directors:
                print(f"{director.id:<5} {director.name:<45}")
        else:
            print("Nenhum diretor encontrado na tabela.")

    @session_manager(commit=True)  # Dá commit, pois altera dados
    def delete(self, where, session):
        return super().delete_with_dependencies(
            where=where,
            related_models=[(MovieDirectorRepository.model, "director_id")]
        )






