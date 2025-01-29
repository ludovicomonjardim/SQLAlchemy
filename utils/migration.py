from sqlalchemy import Table, Column, MetaData, text, inspect, String, Integer
from database import engine

metadata = MetaData()

def coluna_existe(nome_tabela, nome_coluna):
    """Verifica se uma coluna existe em uma tabela específica."""
    inspector = inspect(engine)
    colunas_existentes = {col["name"] for col in inspector.get_columns(nome_tabela)}
    return nome_coluna in colunas_existentes


def atualizar_tabela(nome_tabela, colunas_novas):
    """Atualiza a estrutura de uma tabela, adicionando colunas novas se necessário.

    Args:
        nome_tabela (str): Nome da tabela a ser verificada e atualizada.
        colunas_novas (dict): Dicionário com as novas colunas a serem adicionadas.
            Exemplo: {"diretor": String, "nota": Integer}
    """

    # Verifica quais colunas já existem na tabela
    inspector = inspect(engine)
    colunas_existentes = {col["name"] for col in inspector.get_columns(nome_tabela)}

    # Filtra apenas as colunas que ainda não existem
    colunas_a_adicionar = {
        nome: tipo for nome, tipo in colunas_novas.items() if nome not in colunas_existentes
    }

    if not colunas_a_adicionar:
        print(f"✅ A estrutura da tabela '{nome_tabela}' já está atualizada.")
        return

    print(f"🔄 Atualizando estrutura da tabela '{nome_tabela}'...")

    # Criando nova estrutura da tabela com as novas colunas
    tabela_nova = Table(
        f"{nome_tabela}_novo", metadata,
        Column("id", Integer, primary_key=True),  # Mantemos um ID único
        *[Column(nome, tipo, nullable=False) for nome, tipo in colunas_novas.items()]
    )

    # Criar a nova tabela no banco
    metadata.create_all(engine)

    with engine.connect() as conn:
        # Copiar os dados da tabela antiga para a nova (somente colunas existentes)
        colunas_comuns = set(colunas_novas.keys()).intersection(colunas_existentes)
        colunas_str = ", ".join(colunas_comuns)

        if colunas_comuns:
            conn.execute(text(f"""
                INSERT INTO {tabela_nova.name} ({colunas_str})
                SELECT {colunas_str} FROM {nome_tabela};
            """))

        # Remover a tabela antiga e renomear a nova
        conn.execute(text(f"DROP TABLE {nome_tabela};"))
        conn.execute(text(f"ALTER TABLE {tabela_nova.name} RENAME TO {nome_tabela};"))

    print(f"✅ Estrutura da tabela '{nome_tabela}' atualizada com sucesso!")
