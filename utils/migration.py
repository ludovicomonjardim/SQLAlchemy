from sqlalchemy import MetaData, Table, inspect
from sqlalchemy.orm import Session
from database import engine
from models.base import Base

metadata = MetaData()

def obter_estrutura_modelo(modelo):
    """Obtém a estrutura do modelo ORM."""
    return {col.name: col.type for col in modelo.__table__.columns}

def obter_estrutura_tabela(nome_tabela):
    """Obtém a estrutura da tabela no banco de dados."""
    inspector = inspect(engine)
    colunas = inspector.get_columns(nome_tabela)
    return {col["name"]: col["type"] for col in colunas}

def atualizar_tabela(modelo):
    """Atualiza a estrutura da tabela caso necessário, seguindo a abordagem de tabela temporária."""
    nome_tabela = modelo.__tablename__

    # Obter estruturas
    estrutura_modelo = obter_estrutura_modelo(modelo)
    estrutura_tabela = obter_estrutura_tabela(nome_tabela)

    # Comparar estruturas
    colunas_faltando = set(estrutura_modelo.keys()) - set(estrutura_tabela.keys())
    colunas_excedentes = set(estrutura_tabela.keys()) - set(estrutura_modelo.keys())

    if not colunas_faltando and not colunas_excedentes:
        print(f"A estrutura da tabela '{nome_tabela}' já está atualizada. Nenhuma modificação necessária.")
        return

    # Exibir diferenças
    print(f"Diferenças detectadas na tabela '{nome_tabela}':")
    if colunas_faltando:
        print(f"Colunas a serem adicionadas: {colunas_faltando}")
    if colunas_excedentes:
        print(f"Colunas não previstas no modelo: {colunas_excedentes}")

    # Criar uma tabela temporária
    nome_temp = f"{nome_tabela}_temp"
    modelo.__table__.name = nome_temp  # Alterar o nome da tabela para criar a temporária
    with engine.begin() as conn:
        Base.metadata.create_all(conn, tables=[modelo.__table__])
    print(f"Tabela temporária '{nome_temp}' criada com sucesso.")

    # Importar os dados da tabela original para a tabela temporária
    colunas_comuns = [col for col in estrutura_tabela if col in estrutura_modelo]
    if colunas_comuns:
        with Session(engine) as session:
            tabela_original = Table(nome_tabela, metadata, autoload_with=engine)
            tabela_temp = Table(nome_temp, metadata, autoload_with=engine)

            stmt_select = session.query(*[tabela_original.c[col] for col in colunas_comuns])
            resultados = session.execute(stmt_select).fetchall()

            insert_stmt = tabela_temp.insert().values([dict(zip(colunas_comuns, row)) for row in resultados])
            session.execute(insert_stmt)
            session.commit()

        print(f"Dados copiados da tabela '{nome_tabela}' para '{nome_temp}'.")

    # Remover a tabela original
    with engine.begin() as conn:
        Table(nome_tabela, metadata, autoload_with=conn).drop(conn)
    print(f"Tabela original '{nome_tabela}' removida.")

    # Criar novamente a tabela com o nome original e copiar os dados de volta
    modelo.__table__.name = nome_tabela  # Restaurar o nome correto
    with engine.begin() as conn:
        Base.metadata.create_all(conn, tables=[modelo.__table__])  # Criar a nova tabela com a estrutura correta

    with Session(engine) as session:
        tabela_temp = Table(nome_temp, metadata, autoload_with=engine)
        tabela_final = Table(nome_tabela, metadata, autoload_with=engine)

        stmt_select = session.query(*[tabela_temp.c[col] for col in colunas_comuns])
        resultados = session.execute(stmt_select).fetchall()

        insert_stmt = tabela_final.insert().values([dict(zip(colunas_comuns, row)) for row in resultados])
        session.execute(insert_stmt)
        session.commit()

    # Remover a tabela temporária
    with engine.begin() as conn:
        tabela_temp.drop(conn)
    print(f"Tabela temporária '{nome_temp}' removida. Tabela '{nome_tabela}' foi recriada com sucesso.")

    # Recarregar a estrutura das tabelas
    metadata.clear()
    Base.metadata.reflect(bind=engine)
