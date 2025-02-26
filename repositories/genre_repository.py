"""
repositories/genre_repository.py
Este módulo contém a classe GenreRepository, responsável por interagir com a tabela de gêneros no banco de dados.
"""

from repositories.crud_base_repository import CrudBaseRepository
from repositories.movie_genre_repository import MovieGenreRepository
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
        Exclui um ou mais diretores e suas associações com filmes.
        - Remove todas as dependências antes de excluir o diretor.
        - Usa `delete_with_dependencies()` para garantir exclusão segura.
        """

        return super().delete_with_dependencies(
            where=where,
            related_models=[(MovieGenreRepository.model, "genre_id")]
        )
