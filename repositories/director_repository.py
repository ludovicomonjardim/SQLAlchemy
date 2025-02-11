"""
repositories/director_repository.py
Este módulo contém a classe DirectorRepository, responsável por interagir com a tabela de diretores no banco de dados.
"""

from repositories.crud_base_repository import CrudBaseRepository
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
        """
        Exclui um ou mais diretores e suas associações com filmes.
        - `where` pode ser um dicionário (exclusão única) ou uma lista de filtros (exclusão múltipla).
        - Remove as associações antes de excluir o diretor.
        - Retorna um dicionário indicando sucesso ou falha da operação.
        """

        if not where:
            return {"success": False, "error": "Erro: Nenhum critério de exclusão fornecido."}

        try:
            # Se `where` for um dicionário, usa `filter_by`
            if isinstance(where, dict):
                director_to_delete = session.query(Director).filter_by(**where).first()
                if not director_to_delete:
                    return {"success": False, "error": "Erro: Diretor não encontrado."}

                # Exclui associações do diretor antes de removê-lo
                from repositories.movie_director_repository import MovieDirectorRepository
                movie_director_repo = MovieDirectorRepository()
                result_associations = movie_director_repo.delete({"id": director_to_delete.id}, ignore_if_not_found=True)
                if not result_associations["success"]:
                    return result_associations

                result = super().delete(where)
                if not result["success"]:
                    return result

                return {"success": True, "message": f"Diretor '{director_to_delete.name}' removido com sucesso."}

            # Se `where` for uma lista, usa `filter`
            elif isinstance(where, list):
                query = session.query(Director).filter(*where)
                deleted_count = query.delete(synchronize_session=False)

                if deleted_count == 0:
                    return {"success": False, "error": "Nenhum diretor encontrado para exclusão."}

                return {"success": True, "deleted_count": deleted_count}

            else:
                return {"success": False, "error": "Erro: O parâmetro `where` deve ser um dicionário ou uma lista de filtros."}

        except Exception as e:
            return {"success": False, "error": f"Erro ao excluir registros: {e}"}
