from repositories.crud_base_repository import CrudBaseRepository
from repositories.movie_director_repository import MovieDirectorRepository
from models.director import Director
from utils.session import session_manager

class DirectorRepository(CrudBaseRepository):
    model = Director

    @staticmethod
    @session_manager
    def report(session):
        # Exibe todos os diretores cadastrados no banco de dados.
        directors = session.query(Director).all()
        if directors:
            print("-" * 51)
            print(f"{'Id':<5} {'Nome':<45}")
            print("-" * 51)
            for director in directors:
                print(f"{director.id:<5} {director.name:<45}")
        else:
            print("Nenhum diretor encontrado na tabela.")

    @session_manager
    def delete(self, where, session):
        """
        Exclui um diretor e também remove suas associações na tabela movie_director.

        :param where: Dicionário com as condições para exclusão do ator.
        :param session: Sessão do banco (gerenciada automaticamente).
        :return: Mensagem indicando sucesso ou erro.
        """
        director_to_delete = session.query(Director).filter_by(**where).first()
        if not director_to_delete:
            return "Erro: Diretor não encontrado."

        # Remover todas as associações do ator na tabela movie_directors usando MovieDirectorRepository
        movie_director_repo = MovieDirectorRepository()
        result_associations = movie_director_repo.delete({"id": director_to_delete.id})

        # Verifica se houve erro ao excluir as associações
        if isinstance(result_associations, str):  # Se `delete` retornou um erro
            return result_associations  # Retorna a mensagem de erro

        # Agora podemos remover o ator com segurança
        result = super().delete(where)

        if isinstance(result, str):  # Se `session_manager` retornou um erro
            return result

        return f"Diretor '{director_to_delete.name}' e suas associações foram removidos com sucesso."

