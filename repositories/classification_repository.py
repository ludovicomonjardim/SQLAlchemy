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
        Exclui uma ou mais classificações apenas se não estiverem associadas a filmes.
        - `where` pode ser um dicionário (exclusão única) ou uma lista de filtros (exclusão múltipla).
        - Retorna um dicionário indicando sucesso ou falha da operação.
        """

        if not where:
            return {"success": False, "error": "Erro: Nenhum critério de exclusão fornecido."}

        try:
            if isinstance(where, dict):
                classification_to_delete = session.query(Classification).filter_by(**where).first()
                if not classification_to_delete:
                    return {"success": False, "error": "Erro: Classificação não encontrada."}

                # 🔹 Verifica se há filmes associados
                associated_movies = session.query(Movie).filter(
                    Movie.classification_id == classification_to_delete.id).count()
                if associated_movies > 0:
                    return {"success": False,
                            "error": f"Erro: Não é possível excluir '{classification_to_delete.name}', pois está associada a {associated_movies} filme(s)."}

                # Prossegue com a exclusão se não houver filmes associados
                result = super().delete(where)
                if not result["success"]:
                    return result

                return {"success": True,
                        "message": f"Classificação '{classification_to_delete.name}' removida com sucesso."}

            elif isinstance(where, list):
                # 🔹 Verifica se alguma das classificações na lista está associada a filmes
                classifications_to_delete = session.query(Classification).filter(*where).all()
                for classification in classifications_to_delete:
                    associated_movies = session.query(Movie).filter(Movie.classification_id == classification.id).count()
                    if associated_movies > 0:
                        return {"success": False,
                                "error": f"Erro: Não é possível excluir '{classification.name}', pois está associada a {associated_movies} filme(s)."}

                # Prossegue com a exclusão se nenhuma classificação estiver associada a filmes
                query = session.query(Classification).filter(*where)
                deleted_count = query.delete(synchronize_session=False)

                if deleted_count == 0:
                    return {"success": False, "error": "Nenhuma classificação encontrada para exclusão."}

                return {"success": True, "deleted_count": deleted_count}

            else:
                return {"success": False,
                        "error": "Erro: O parâmetro `where` deve ser um dicionário ou uma lista de filtros."}

        except Exception as e:
            return {"success": False, "error": f"Erro ao excluir registros: {e}"}
