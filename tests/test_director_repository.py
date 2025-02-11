import pytest
from sqlalchemy.exc import IntegrityError
from repositories.director_repository import DirectorRepository
from models.director import Director
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
def director_repo(session):
    """Instancia o repositório de diretores para os testes."""
    return DirectorRepository()


def test_insert_director(director_repo, session):
    """Testa a inserção de um diretor."""
    director = {"name": "Christopher Nolan"}
    director_repo.insert(director)

    inserted_director = session.query(Director).filter_by(name="Christopher Nolan").first()
    assert inserted_director is not None
    assert inserted_director.name == "Christopher Nolan"


def test_update_director(director_repo, session):
    """Testa a atualização do nome de um diretor garantindo que os nomes não existam previamente."""

    # Remove qualquer diretor com os nomes envolvidos no teste para evitar conflitos
    session.query(Director).filter(Director.name.in_(["Steven", "Steven Spielberg"])).delete(synchronize_session=False)
    session.commit()

    # Insere um diretor com um nome único
    director_repo.insert({"name": "Steven"})
    inserted_director = session.query(Director).filter_by(name="Steven").first()

    # Atualiza o nome do diretor
    director_repo.update(where={"name": "Steven"}, with_={"name": "Steven Spielberg"})
    session.expire_all()
    updated_director = session.query(Director).filter_by(id=inserted_director.id).first()

    # Valida se o nome foi atualizado corretamente
    assert updated_director.name == "Steven Spielberg"


def test_delete_director(director_repo, session):
    """Testa a remoção de um diretor."""
    director_repo.insert({"name": "Quentin Tarantino"})
    inserted_director = session.query(Director).filter_by(name="Quentin Tarantino").first()
    assert inserted_director is not None

    director_repo.delete(where={"name": "Quentin Tarantino"})
    deleted_director = session.query(Director).filter_by(name="Quentin Tarantino").first()
    assert deleted_director is None


def test_unique_constraint(director_repo, session):
    """Testa a restrição de unicidade no nome do diretor."""

    # Remove o diretor se já existir para garantir um teste limpo
    session.query(Director).filter(Director.name == "Martin Scorsese").delete(synchronize_session=False)
    session.commit()

    # Insere o diretor pela primeira vez (deve ter sucesso)
    result1 = director_repo.insert({"name": "Martin Scorsese"})
    assert result1["success"] is True, f"Falha na primeira inserção: {result1['error']}"

    # Tenta inserir o mesmo nome novamente (deve falhar)
    result2 = director_repo.insert({"name": "Martin Scorsese"})

    assert result2["success"] is False, "A inserção duplicada deveria falhar, mas foi bem-sucedida."
    assert "Violação de integridade" in result2["error"], f"Erro inesperado: {result2['error']}"
