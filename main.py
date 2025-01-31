from database import initialize_database, get_connection
from repositories.filme_repository import FilmeRepository
from sqlalchemy import text


def pausa(listar=True):
    """
    Pausa a execução do programa até que o usuário pressione Enter.

    Args:
        listar (bool, opcional): Se True, imprime todos os filmes antes de pausar.
                                 Padrão é True.
    """
    if listar:
        tb_filmes.print_all()
    input("\nTecle Enter para continuar...")
    clear_screen()


def clear_screen():
    """
    Limpa a tela do console, imprimindo múltiplas quebras de linha.
    """
    print("\n" * 10)


# Inicializar o banco de dados
initialize_database()

# Inicializa o repositório de filmes e atualiza a estrutura da tabela
tb_filmes = FilmeRepository()
tb_filmes.atualiza()

# USANDO SQL PURO
print("\nLISTANDO todos os filmes como SQL puro...")
"""
ATENÇÃO!!
O que segue em relação ao uso de SQL PURO é apenas uma demonstração de 
recurso. Seu uso pode trazer problemas de compatibilidade entre bancos 
diferentes. O ideal é padronizar todas as consultas via ORM. 
"""
with get_connection() as conn:
    try:
        result = conn.execute(text("SELECT * FROM filmes;"))
        for row in result:
            print(row)
    except Exception as e:
        print(f"Erro ao executar SQL puro: {e}")
pausa(False)

# LISTA O CONTEÚDO DA TABELA
print("\nLISTANDO todos os filmes...")
tb_filmes.print_all()
pausa(False)

# INSERT
print("\nINSERINDO um novo filme...")
tb_filmes.insert({"titulo": "Matrix", "genero": "Ficção", "ano": 1999})
pausa()

# UPDATE
print("\nATUALIZANDO o ano do filme Matrix...")
rows_updated = tb_filmes.update(where={"titulo": "Matrix"}, with_={"ano": 2001})
if rows_updated:
    print(f"{rows_updated} filme(s) atualizado(s).")
pausa()

# DELETE
print("\nDELETANDO o filme Matrix...")
tb_filmes.delete(where={"titulo": "Matrix"})
pausa()

# QUERY
print("\nCONSULTANDO filmes do gênero 'Drama'...")
filmes = tb_filmes.get_by_field(where={"genero": "Drama"})
for filme in filmes:
    print(filme)  # Agora os dicionários não terão `_sa_instance_state`
pausa()
