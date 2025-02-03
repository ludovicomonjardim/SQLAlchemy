import pytest
from database import initialize_database, get_connection

def test_database_connection():
    """Testa se a conexão com o banco de dados pode ser estabelecida"""
    initialize_database()
    with get_connection() as conn:
        assert conn is not None
