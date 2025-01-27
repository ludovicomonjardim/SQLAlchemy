
from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/cinema"

# ESTRUTURA DO DATABASE_URL:
# postgresql: Dialeto
# psycopg2..: Driver
# Usuário...: postgres
# Senha.....: admin
# Porta.....: 5432
# Banco.....: cinema

# Criação da engine
engine = create_engine(DATABASE_URL)



# Testando a conexão
try:
    conn = engine.connect()
    print("\nConexão bem-sucedida!")
except Exception as e:
    raise f"Erro ao conectar ao banco de dados: {e}"

# Faz uma consulta usando SQL
result = conn.execute(text('SELECT * FROM public.filmes;'))

# Exibe o resultado da consulta ao banco
for row in result:
    print(row, row.titulo)

# Fecha a conexão com o banco
conn.close()
print("Conexão encerrada.\n")


# O RECOMENDAD É O USO DE SESSION (para garantir o fechamento correto), COMO SEGUE:
Session = sessionmaker(bind=engine)
try:
    with Session() as session:
        print("\nConexão bem-sucedida!")
        result = session.execute(text('SELECT * FROM filmes;'))
        for row in result:
            print(row, row.titulo)
except Exception as e:
    raise f"Erro ao conectar ao banco de dados: {e}"
print("Conexão encerrada automaticamente.")




class Base(DeclarativeBase):
    pass

class Filme(Base):
    __tablename__ = "filmes"
    titulo = Column(String, nullable=False, primary_key=True)
    genero = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)

# Criar tabelas
Base.metadata.create_all(engine)

# Sessão para interagir com o banco
Session = sessionmaker(bind=engine)
with Session() as session:
    # Inserindo dados
    novo_filme = Filme(titulo="Matrix", genero="Ficção", ano=1999)
    session.add(novo_filme)
    session.commit()

    # Consultando dados
    filmes = session.query(Filme).all()
    for filme in filmes:
        print(filme.titulo, filme.genero, filme.ano)