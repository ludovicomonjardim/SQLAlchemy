import os
from models.base import Base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

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

import logging
from utils.logging_config import setup_logger

# Configura o logger
setup_logger()

# Verifica se está rodando dentro do Docker
DOCKER_ENV = os.getenv("DOCKER_ENV", "false").lower() == "true"
description = ""

# Verifica se está rodando testes e escolhe o banco adequado
if os.getenv("PYTEST_RUNNING", "false").lower() == "true":
    DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/test_cinema"
    decription = "Banco de testes"
elif DOCKER_ENV:
    DATABASE_URL = "postgresql+psycopg2://postgres:admin@db:5432/cinema"
    description = "Banco do Docker"
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:admin@localhost:5432/cinema")
    description = "Banco local"

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não definida e não estamos rodando no Docker.")

# Forçar o uso do banco de testes ao rodar initialize_database()
if "PYTEST_RUNNING" not in os.environ:
    os.environ["PYTEST_RUNNING"] = "true"
    description = "Banco de testes"

logging.info(f"Using database: {description.upper()} - URL: {DATABASE_URL}")

# Criando a engine
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)

# Criador de sessão
Session = sessionmaker(bind=engine)

def get_session():
    """Retorna uma nova sessão do banco de dados."""
    return Session()


def initialize_database():
    """Cria as tabelas do banco de dados garantindo que todas sejam removidas antes."""

    logging.info("🔹 Inicializando banco...")

    with engine.connect() as connection:
        logging.info("Removendo todas as tabelas existentes com CASCADE...")
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
        connection.commit()

    # logging.info("Criando tabelas na ordem correta...")
    # Classification.__table__.create(engine, checkfirst=True)
    # Genre.__table__.create(engine, checkfirst=True)
    # Director.__table__.create(engine, checkfirst=True)
    # Actor.__table__.create(engine, checkfirst=True)
    #
    # Movie.__table__.create(engine, checkfirst=True)
    # MovieGenre.__table__.create(engine, checkfirst=True)
    # MovieDirector.__table__.create(engine, checkfirst=True)
    # MovieActor.__table__.create(engine, checkfirst=True)
    #
    # CinemaSession.__table__.create(engine, checkfirst=True)
    # Ticket.__table__.create(engine, checkfirst=True)

    logging.info("🔹 Criando todas as tabelas...")

    # 🔹 Criar todas as tabelas corretamente
    Base.metadata.create_all(engine)

    logging.info("✅ Todas as tabelas foram criadas com sucesso!")


@contextmanager
def get_connection():
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()
