from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.base import Base


# Configuração do banco de dados
DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/cinema"

# Criação da engine
engine = create_engine(DATABASE_URL)

# Configuração do sessionmaker
Session = sessionmaker(bind=engine)

conn = engine.connect()

# Função para inicializar o banco de dados
def initialize_database():
    """Cria todas as tabelas no banco de dados com base nos modelos."""
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")


# class Database():
#     def __init__(self):
#         # Configuração do banco de dados
#         # DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/cinema"
#
#         # Criação da engine
#         self.engine = create_engine(DATABASE_URL)
#
#         self.conn = self.engine.connect()
#
#         # Configuração do sessionmaker
#         self.Session = sessionmaker(bind=self.engine)
#
#     def initialize_database(self):
#         """Cria todas as tabelas no banco de dados com base nos modelos."""
#         Base.metadata.create_all(self.engine)
#         print("Tabelas criadas com sucesso!")
