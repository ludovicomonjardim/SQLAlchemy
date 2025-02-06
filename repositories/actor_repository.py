from repositories.crud_base_repository import CrudBaseRepository
from models.actor import Actor
from utils.session import session_manager


class ActorRepository(CrudBaseRepository):
    model = Actor  # Definição do modelo correto

    @staticmethod
    @session_manager
    def print_all(session):
        """Exibe todos os atores cadastrados."""
        actors = session.query(Actor).all()
        if actors:
            print()
            print("-" * 51)
            print(f"{'ID':<5} {'Nome':<45}")
            print("-" * 51)
            for actor in actors:
                print(f"{actor.id:<5} {actor.name:<45}")
        else:
            print("Nenhum ator encontrado na tabela.")

    @session_manager
    def insert(self, data, session):
        result = super().insert(data)
        if isinstance(result, str):  # Se `session_manager` retornou um erro, exibimos a mensagem
            print(result)  # Exibe a mensagem de erro
        else:
            print(f"Ator '{data['name']}' inserido com sucesso.")
        return result
