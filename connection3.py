
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.exc import SQLAlchemyError


def exibe_filmes(Session):
    with Session() as session:
        for filme in session.query(Filme).yield_per(50):  # Processa 50 registros por vez:
            print(filme)

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
        return f"Filme - Título: {self.titulo}\t | Gênero: {self.genero} | Ano: {self.ano}"


# Configuração do banco
DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/cinema"
# echo=True Mostra as queries no console
engine = create_engine(DATABASE_URL)

# Criar tabelas
Base.metadata.create_all(engine)


print("\nUsando session direto - NÃO RECOMENDADO")
# Cria a Session que é uma classe para interagir com o banco
Session = sessionmaker(bind=engine)
# Cria o objeto da classe Session para a interaçaõ
session1 = Session()
try:
    # Result recebe o resultado da query
    result = session1.query(Filme).all()
    # Varre o result imprimindo os campos
    for filme in result:
        print(filme, filme.titulo)
finally:
    session1.close()



print("\nUsando session com o with")
with Session() as session:
    for filme in session.query(Filme).yield_per(50):  # Processa 50 registros por vez:
        print(filme, filme.titulo)


print("\nUsando session com o with e com filter")
with Session() as session:
    for filme in session.query(Filme).filter(Filme.titulo.like('P%')).yield_per(50):  # Processa 50 registros por vez
        print(filme, filme.titulo)


# Inserindo dados
print("\nInserindo usando session com o with")
with Session() as session:
    try:
        novo_filme = Filme(titulo="Batman", genero="Ficção", ano=2000)
        session.add(novo_filme)
        session.commit()
    except SQLAlchemyError as e:
        # Reverter as alterações em caso de erro
        session.rollback()
        print(f"Erro ao inserir o filme: {e}")
exibe_filmes(Session)

# Excluindo dados
print("\nExcluindo usando session com o with")
with Session() as session:
    try:
        session.query(Filme).filter(Filme.titulo=="Batman").delete()
        session.commit()
    except SQLAlchemyError as e:
        # Reverter as alterações em caso de erro
        session.rollback()
        print(f"Erro ao inserir o filme: {e}")
exibe_filmes(Session)



# ATUALIZANDO - UPDATE
# with Session() as session:
#     try:
#         session.query(Filme).filter(Filme.titulo=="Batman").delete()
#         session.commit()
#     except SQLAlchemyError as e:
#         # Reverter as alterações em caso de erro
#         session.rollback()
#         print(f"Erro ao inserir o filme: {e}")
#
# with Session() as session:
#     for filme in session.query(Filme).yield_per(50):  # Processa 50 registros por vez:
#         print(filme, filme.titulo)
