from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from models.base import Base
import os

# Configuração do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:admin@localhost:5432/cinema")
# DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/cinema"

# Criação da engine
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)


# Configuração do sessionmaker
Session = sessionmaker(bind=engine)

# Função para inicializar o banco de dados
def initialize_database():
    """Cria todas as tabelas no banco de dados com base nos modelos."""
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")

@contextmanager
def get_connection():
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()