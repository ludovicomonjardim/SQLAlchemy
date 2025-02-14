import pytest
from sqlalchemy.exc import IntegrityError
from repositories.classification_repository import ClassificationRepository
from models.classification import Classification
from models.movie import Movie
from database import initialize_database, get_session


@pytest.fixture(scope="function")
def session():
    """Cria uma sessão temporária para os testes e garante rollback ao final."""
    initialize_database()
    session = get_session()
    yield session
    session.rollback()  # 🔹 Reverte todas as alterações feitas no teste
    session.close()


@pytest.fixture(scope="function")
def classification_repo(session):
    """Instancia o repositório de classificações para os testes."""
    return ClassificationRepository()


def test_insert_classification(classification_repo, session):
    """Testa a inserção de uma classificação etária garantindo que não exista duplicação."""

    # 🔹 Remove a classificação caso já exista
    session.query(Classification).filter_by(name="Livre").delete(synchronize_session=False)
    session.commit()

    # 🔹 Insere uma nova classificação
    classification_data = {
        "name": "Livre",
        "description": "Permitido para todos os públicos",
        "min_age": 0
    }
    classification_repo.insert(classification_data)

    # 🔹 Verifica se a inserção foi bem-sucedida
    inserted_classification = session.query(Classification).filter_by(name="Livre").first()
    assert inserted_classification is not None
    assert inserted_classification.description == "Permitido para todos os públicos"
    assert inserted_classification.min_age == 0


def test_update_classification(classification_repo, session):
    """Testa a atualização de uma classificação etária garantindo que não haja conflitos."""

    # 🔹 Remove qualquer classificação existente com os nomes do teste
    session.query(Classification).filter(Classification.name.in_(["Livre", "Sem Restrição"])).delete(synchronize_session=False)
    session.commit()

    # 🔹 Insere uma classificação com um nome único
    classification_repo.insert({"name": "Livre", "description": "Permitido para todos os públicos", "min_age": 0})
    inserted_classification = session.query(Classification).filter_by(name="Livre").first()

    # 🔹 Atualiza o nome da classificação
    classification_repo.update(where={"id": inserted_classification.id}, with_={"name": "Sem Restrição"})
    session.expire_all()
    updated_classification = session.query(Classification).filter_by(id=inserted_classification.id).first()

    # 🔹 Valida se o nome foi atualizado corretamente
    assert updated_classification.name == "Sem Restrição"


def test_delete_classification(classification_repo, session):
    """Testa a remoção de uma classificação etária sem associações."""

    # 🔹 Remove qualquer resíduo de testes anteriores
    session.query(Classification).filter_by(name="18 anos").delete(synchronize_session=False)
    session.commit()

    # 🔹 Insere a classificação e verifica se existe
    classification_repo.insert({"name": "18 anos", "description": "Somente para maiores de idade", "min_age": 18})
    inserted_classification = session.query(Classification).filter_by(name="18 anos").first()
    assert inserted_classification is not None

    # 🔹 Exclui a classificação e verifica se foi removida
    classification_repo.delete(where={"id": inserted_classification.id})
    deleted_classification = session.query(Classification).filter_by(id=inserted_classification.id).first()
    assert deleted_classification is None


def test_unique_constraint(classification_repo, session):
    """Testa a restrição de unicidade no nome da classificação."""

    # 🔹 Remove a classificação se já existir para garantir um teste limpo
    session.query(Classification).filter_by(name="16 anos").delete(synchronize_session=False)
    session.commit()

    # 🔹 Insere a classificação pela primeira vez (deve ter sucesso)
    result1 = classification_repo.insert({"name": "16 anos", "description": "Não recomendado para menores de 16 anos", "min_age": 16})
    assert result1["success"] is True, f"Falha na primeira inserção: {result1['error']}"

    # 🔹 Tenta inserir a mesma classificação novamente (deve falhar)
    result2 = classification_repo.insert({"name": "16 anos", "description": "Não recomendado para menores de 16 anos", "min_age": 16})

    assert result2["success"] is False, "A inserção duplicada deveria falhar, mas foi bem-sucedida."
    assert "Violação de integridade" in result2["error"], f"Erro inesperado: {result2['error']}"


def test_delete_classification_with_movie(classification_repo, session):
    """Testa a remoção de uma classificação que está associada a um filme."""

    # 🔹 Insere uma classificação e verifica se existe
    classification_repo.insert({"name": "12 anos", "description": "Não recomendado para menores de 12 anos", "min_age": 12})
    inserted_classification = session.query(Classification).filter_by(name="12 anos").first()

    # 🔹 Associa a classificação a um filme
    session.add(Movie(title="Filme Teste", year=2023, duration=120, classification_id=inserted_classification.id, rating=8, active=True))
    session.commit()

    # 🔹 Tenta excluir a classificação associada a um filme
    result = classification_repo.delete({"id": inserted_classification.id})

    assert result["success"] is False
    assert "pois está associada a" in result["error"]  # Corrigida a verificação da mensagem de erro
