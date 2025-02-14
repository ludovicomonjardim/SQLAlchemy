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
    session.rollback()  # Reverte todas as alterações feitas no teste
    session.close()


@pytest.fixture(scope="function")
def classification_repo(session):
    """Instancia o repositório de classificações para os testes."""
    return ClassificationRepository()


def test_insert_classification(classification_repo, session):
    """Testa a inserção de uma classificação etária garantindo que não exista duplicação."""

    # Verifica se já existe e não tenta excluí-la se houver filmes associados
    existing_classification = session.query(Classification).filter_by(name="Livre").first()

    if existing_classification is None:
        classification_data = {
            "name": "Livre",
            "description": "Permitido para todos os públicos",
            "min_age": 0
        }
        classification_repo.insert(classification_data)

        inserted_classification = session.query(Classification).filter_by(name="Livre").first()
        assert inserted_classification is not None
        assert inserted_classification.description == "Permitido para todos os públicos"
        assert inserted_classification.min_age == 0


def test_update_classification(classification_repo, session):
    """Testa a atualização de uma classificação etária garantindo que não haja conflitos."""

    # Verifica se há classificação "Livre"
    classification = session.query(Classification).filter_by(name="Livre").first()

    assert classification is not None, "A classificação 'Livre' deveria existir antes da atualização."

    # Captura o ID da classificação original
    classification_id = classification.id

    # Realiza a atualização no banco e verifica o retorno
    result = classification_repo.update(where={"id": classification_id}, with_={"name": "Sem Restrição"})

    # Verifica se a atualização foi bem-sucedida
    assert result["success"], f"Falha ao atualizar: {result.get('error', 'Erro desconhecido')}"

    # Commit explícito para persistir a mudança
    session.commit()

    # Expira a sessão para garantir que a consulta obtenha os dados mais recentes
    session.expire_all()

    # Recarrega os dados mais recentes
    updated_classification = session.query(Classification).filter_by(id=classification_id).first()
    session.refresh(updated_classification)

    assert updated_classification is not None, "A classificação deveria existir após a atualização."
    assert updated_classification.name == "Sem Restrição", f"Esperado: 'Sem Restrição', Obtido: {updated_classification.name}"


def test_delete_classification(classification_repo, session):
    """Testa a remoção de uma classificação etária sem associações."""

    # Verifica se "18 anos" já existe e se pode ser removida
    classification = session.query(Classification).filter_by(name="18 anos").first()

    if classification:
        associated_movies = session.query(Movie).filter_by(classification_id=classification.id).count()

        if associated_movies == 0:
            classification_repo.delete(where={"id": classification.id})
            deleted_classification = session.query(Classification).filter_by(id=classification.id).first()
            assert deleted_classification is None


def test_unique_constraint(classification_repo, session):
    """Testa a restrição de unicidade no nome da classificação."""

    classification = session.query(Classification).filter_by(name="16 anos").first()

    if classification is None:
        result1 = classification_repo.insert(
            {"name": "16 anos", "description": "Não recomendado para menores de 16 anos", "min_age": 16})
        assert result1["success"] is True, f"Falha na primeira inserção: {result1['error']}"

        # Tenta inserir a mesma classificação novamente (deve falhar)
        result2 = classification_repo.insert(
            {"name": "16 anos", "description": "Não recomendado para menores de 16 anos", "min_age": 16})

        assert result2["success"] is False, "A inserção duplicada deveria falhar, mas foi bem-sucedida."
        assert "Violação de integridade" in result2["error"], f"Erro inesperado: {result2['error']}"


def test_delete_classification_with_movie(classification_repo, session):
    """Testa a remoção de uma classificação que está associada a um filme."""

    classification = session.query(Classification).filter_by(name="12 anos").first()

    if classification is None:
        classification_repo.insert(
            {"name": "12 anos", "description": "Não recomendado para menores de 12 anos", "min_age": 12})
        classification = session.query(Classification).filter_by(name="12 anos").first()

    # Associa a classificação a um filme, se necessário
    associated_movies = session.query(Movie).filter_by(classification_id=classification.id).count()

    if associated_movies == 0:
        session.add(Movie(title="Filme Teste", year=2023, duration=120, classification_id=classification.id, rating=8,
                          active=True))
        session.commit()

    # Tenta excluir a classificação associada a um filme
    result = classification_repo.delete({"id": classification.id})

    assert result["success"] is False
    assert "pois está associada a" in result["error"]  # Corrigida a verificação da mensagem de erro
