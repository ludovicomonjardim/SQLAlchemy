from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from models.base import Base

# IMPORTANDO TODOS OS MODELOS AQUI PARA EVITAR ERRO DE REFERÊNCIA
from models.actor import Actor
from models.classification import Classification
from models.director import Director
from models.genre import Genre
from models.movie import Movie
from models.movie_actor import MovieActor
from models.movie_director import MovieDirector
from models.movie_genre import MovieGenre
from models.cinema_session import CinemaSession
from models.ticket import Ticket

import os

# from sqlalchemy.orm import sessionmaker



# Configuração do banco de dados
if os.getenv("DOCKER_ENV") == "true":
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:admin@db:5432/cinema")
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:admin@localhost:5432/cinema")

print(f"Using database URL: {DATABASE_URL}")


# Criando a engine
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)

# Criador de sessão
Session = sessionmaker(bind=engine)

def get_session():
    """Retorna uma nova sessão do banco de dados."""
    return Session()


def initialize_database():
    """Cria as tabelas do banco de dados garantindo a ordem correta."""
    print("Criando tabelas na ordem correta...")
    # Base.metadata.create_all(engine)

    # Usando __table__.create() ao invés de Base.metadata.create_all(engine)
    # para garantir a ordem de criação das tabelas
    Classification.__table__.create(engine, checkfirst=True)
    Genre.__table__.create(engine, checkfirst=True)
    Director.__table__.create(engine, checkfirst=True)
    Actor.__table__.create(engine, checkfirst=True)

    # Criar tabelas que dependem das anteriores
    Movie.__table__.create(engine, checkfirst=True)
    MovieGenre.__table__.create(engine, checkfirst=True)
    MovieDirector.__table__.create(engine, checkfirst=True)
    MovieActor.__table__.create(engine, checkfirst=True)

    CinemaSession.__table__.create(engine, checkfirst=True)
    Ticket.__table__.create(engine, checkfirst=True)

    print("Todas as tabelas foram criadas com sucesso!")


@contextmanager
def get_connection():
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()
