import pytest
from sqlalchemy.exc import IntegrityError
from repositories.genre_repository import GenreRepository
from models.genre import Genre
from database import initialize_database, get_session


@pytest.fixture(scope="function")
def session():
    """Cria uma sessão temporária para os testes."""
    initialize_database()
    session = get_session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def genre_repo(session):
    """Instancia o repositório de gêneros para os testes."""
    return GenreRepository()


def test_insert_genre(genre_repo, session):
    """Testa a inserção de um gênero."""
    genre = {"name": "Ação"}
    genre_repo.insert(genre)

    inserted_genre = session.query(Genre).filter_by(name="Ação").first()
    assert inserted_genre is not None
    assert inserted_genre.name == "Ação"


def test_update_genre(genre_repo, session):
    """Testa a atualização do nome de um gênero garantindo que os nomes não existam previamente."""

    # Remove qualquer gênero com os nomes envolvidos no teste para evitar conflitos
    session.query(Genre).filter(Genre.name.in_(["Sci-Fi", "Ficção Científica"])).delete(synchronize_session=False)
    session.commit()

    # Insere um gênero com um nome único
    genre_repo.insert({"name": "Sci-Fi"})
    inserted_genre = session.query(Genre).filter_by(name="Sci-Fi").first()

    # Atualiza o nome do gênero
    genre_repo.update(where={"name": "Sci-Fi"}, with_={"name": "Ficção Científica"})
    session.expire_all()
    updated_genre = session.query(Genre).filter_by(id=inserted_genre.id).first()

    # Valida se o nome foi atualizado corretamente
    assert updated_genre.name == "Ficção Científica"


def test_delete_genre(genre_repo, session):
    """Testa a remoção de um gênero."""
    genre_repo.insert({"name": "Terror"})
    inserted_genre = session.query(Genre).filter_by(name="Terror").first()
    assert inserted_genre is not None

    genre_repo.delete(where={"name": "Terror"})
    deleted_genre = session.query(Genre).filter_by(name="Terror").first()
    assert deleted_genre is None


def test_unique_constraint(genre_repo, session):
    """Testa a restrição de unicidade no nome do gênero."""

    # Remove o gênero se já existir para garantir um teste limpo
    session.query(Genre).filter(Genre.name == "Drama").delete(synchronize_session=False)
    session.commit()

    # Insere o gênero pela primeira vez (deve ter sucesso)
    result1 = genre_repo.insert({"name": "Drama"})
    assert result1["success"] is True, f"Falha na primeira inserção: {result1['error']}"

    # Tenta inserir o mesmo nome novamente (deve falhar)
    result2 = genre_repo.insert({"name": "Drama"})

    assert result2["success"] is False, "A inserção duplicada deveria falhar, mas foi bem-sucedida."
    assert "Violação de integridade" in result2["error"], f"Erro inesperado: {result2['error']}"
