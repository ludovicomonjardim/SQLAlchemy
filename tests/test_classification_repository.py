import pytest
import logging
import random
import string
from sqlalchemy.exc import IntegrityError
from models.classification import Classification
from repositories.classification_repository import ClassificationRepository

# Configuração do logger
logging.basicConfig(
    filename="test_classification_repository.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

@pytest.fixture(scope="function")
def classification_repo(session):
    """Retorna uma instância do repositório de classificações."""
    return ClassificationRepository()

def generate_random_name():
    """Gera um nome aleatório para garantir unicidade nos testes."""
    return "Teste " + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))

def test_insert_classification(classification_repo, session):
    """Testa a inserção de uma classificação etária garantindo unicidade."""
    random_name = generate_random_name()

    logging.info(f"Tentando inserir classificação com nome: {random_name}")

    result = classification_repo.insert({"name": random_name, "description": "Teste aleatório"})

    assert result["success"], f"Falha na inserção: {result.get('error', 'Erro desconhecido')}"

    inserted = session.query(Classification).filter_by(name=random_name).first()
    assert inserted is not None, "A classificação inserida deveria existir."

    # Limpeza
    session.delete(inserted)
    session.commit()
