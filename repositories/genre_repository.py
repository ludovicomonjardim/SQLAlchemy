"""
repositories/genre_repository.py
Este módulo contém a classe GenreRepository, responsável por interagir com a tabela de gêneros no banco de dados.
"""

from repositories.crud_base_repository import CrudBaseRepository
from models.genre import Genre
from utils.session import session_manager


class GenreRepository(CrudBaseRepository):
    """
    Classe responsável por operações específicas relacionadas ao modelo Genre no banco de dados.
    Herda métodos genéricos de CrudBaseRepository e implementa funcionalidades específicas, como relatórios e exclusão.
    """
    model = Genre

    @staticmethod
    @session_manager(commit=False)  # Não dá commit, pois apenas faz leitura
    def report(session):
        """
        Exibe todos os gêneros cadastrados no banco de dados.
        - A função recebe uma sessão do banco de dados como argumento.
        - Consulta todos os registros da tabela 'Genre'.
        - Se houver gêneros, exibe-os em um formato tabular.
        - Caso contrário, informa que nenhum gênero foi encontrado.
        """
        genres = session.query(Genre).all()
        if genres:
            print("-" * 51)
            print(f"{'ID':<5} {'Nome':<45}")
            print("-" * 51)
            for genre in genres:
                print(f"{genre.id:<5} {genre.name:<45}")
        else:
            print("Nenhum gênero encontrado na tabela.")

    @session_manager(commit=True)  # Dá commit, pois altera dados
    def delete(self, where, session):
        """
        Exclui um ou mais gêneros e suas associações com filmes.
        - `where` pode ser um dicionário (exclusão única) ou uma lista de filtros (exclusão múltipla).
        - Remove as associações antes de excluir o gênero.
        - Retorna um dicionário indicando sucesso ou falha da operação.
        """

        if not where:
            return {"success": False, "error": "Erro: Nenhum critério de exclusão fornecido."}

        try:
            # Se `where` for um dicionário, usa `filter_by`
            if isinstance(where, dict):
                genre_to_delete = session.query(Genre).filter_by(**where).first()
                if not genre_to_delete:
                    return {"success": False, "error": "Erro: Gênero não encontrado."}

                # Exclui associações do gênero antes de removê-lo
                from repositories.movie_genre_repository import MovieGenreRepository
                movie_genre_repo = MovieGenreRepository()
                result_associations = movie_genre_repo.delete({"id": genre_to_delete.id}, ignore_if_not_found=True)
                if not result_associations["success"]:
                    return result_associations

                result = super().delete(where)
                if not result["success"]:
                    return result

                return {"success": True, "message": f"Gênero '{genre_to_delete.name}' removido com sucesso."}

            # Se `where` for uma lista, usa `filter`
            elif isinstance(where, list):
                query = session.query(Genre).filter(*where)
                deleted_count = query.delete(synchronize_session=False)

                if deleted_count == 0:
                    return {"success": False, "error": "Nenhum gênero encontrado para exclusão."}

                return {"success": True, "deleted_count": deleted_count}

            else:
                return {"success": False,
                        "error": "Erro: O parâmetro `where` deve ser um dicionário ou uma lista de filtros."}

        except Exception as e:
            return {"success": False, "error": f"Erro ao excluir registros: {e}"}
