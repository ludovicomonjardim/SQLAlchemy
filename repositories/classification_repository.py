from repositories.crud_base_repository import CrudBaseRepository
from models.classification import Classification
from utils.session import session_manager

class CalssificationRepository(CrudBaseRepository):
    model = Classification

    @staticmethod
    @session_manager
    def print_all(session):
        # Exibe todos os gêneros cadastrados no banco de dados.
        classifications = session.query(Classification).all()
        if classifications:
            print()
            print("-" * 30)
            print(f"{'ID':<5} {'Nome':<50} {"Age":<5} {'Descripltion':<50}")
            print("-" * 115)
            for classification in classifications:
                print(f"{classification.id:<5} {classification.name:<50} {classification.min_age:<5}  {classification.description:<50}")
        else:
            print("Nenhuma classificação encontrada na tabela.")