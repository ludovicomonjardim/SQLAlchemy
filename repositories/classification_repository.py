"""
repositories/classification_repository.py
Este módulo contém a classe ClassificationRepository, responsável por interagir com a tabela de classificações no banco de dados.
"""

from repositories.crud_base_repository import CrudBaseRepository
from models.classification import Classification
from models.movie import Movie
from utils.session import session_manager


class ClassificationRepository(CrudBaseRepository):
    """
    Classe responsável por operações específicas relacionadas ao modelo Classification no banco de dados.
    Herda métodos genéricos de CrudBaseRepository e implementa funcionalidades específicas, como relatórios e exclusão.
    """
    model = Classification

    @staticmethod
    @session_manager(commit=False)  # Apenas leitura, sem commit
    def report(session):
        """
        Exibe todas as classificações cadastradas no banco de dados.
        - A função recebe uma sessão do banco de dados como argumento.
        - Consulta todos os registros da tabela 'Classification'.
        - Se houver classificações, exibe-as em um formato tabular.
        - Caso contrário, informa que nenhuma classificação foi encontrada.
        """
        classifications = session.query(Classification).all()
        if classifications:
            print("-" * 80)
            print(f"{'ID':<5} {'Nome':<20} {'Descrição':<40} {'Idade Mínima':<10}")
            print("-" * 80)
            for classification in classifications:
                print(
                    f"{classification.id:<5} {classification.name:<20} {classification.description:<40} {classification.min_age:<10}")
        else:
            print("Nenhuma classificação encontrada na tabela.")


    @session_manager(commit=True)  # Dá commit, pois altera dados
    def delete(self, where, session):
        """
        Exclui uma ou mais classificações, removendo primeiro associações com filmes.
        - Usa `delete_with_dependencies()` para garantir a exclusão segura.
        """

        return super().delete_with_dependencies(
            where=where,
            related_models=[(Movie, "classification_id")]
        )