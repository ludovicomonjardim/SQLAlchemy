from repositories.crud_base_repository import CrudBaseRepository
from models.genre import Genre
from utils.session import session_manager

class GenreRepository(CrudBaseRepository):
    model = Genre

    @staticmethod
    @session_manager
    def print_all(session):
        # Exibe todos os gêneros cadastrados no banco de dados.
        genres = session.query(Genre).all()
        if genres:
            print()
            print("-" * 30)
            print(f"{'ID':<5} {'Nome':<20}")
            print("-" * 30)
            for genre in genres:
                print(f"{genre.id:<5} {genre.name:<20}")
        else:
            print("Nenhum gênero encontrado na tabela.")