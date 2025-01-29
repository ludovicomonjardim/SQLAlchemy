
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Base declarativa
class Base(DeclarativeBase):
    pass


# Modelo para a tabela "filmes"
# Herda da classe Base que herda da classe DeclarativeBase
class Filme(Base):
    # Define o nome da tabela
    __tablename__ = "filmes"
    # Defina as colunas da tabela como atributos
    titulo = Column(String, primary_key=True)
    genero = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Filme - Título: {self.titulo}, Ano: {self.ano}"


# Configuração do banco
DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/cinema"
engine = create_engine(DATABASE_URL)

# Criar tabelas
Base.metadata.create_all(engine)

# Sessão para interagir com o banco
Session = sessionmaker(bind=engine)
with Session() as session:
    # Inserindo dados
    novo_filme = Filme(titulo="Batman", genero="Ficção", ano=2000)
    session.add(novo_filme)
    session.commit()

    # Consultando dados
    filmes = session.query(Filme).all()
    for filme in filmes:
        print(filme.titulo, filme.genero, filme.ano)

