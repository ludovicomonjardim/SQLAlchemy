from database import initialize_database, get_connection
from repositories.movie_repository import movieRepository
from sqlalchemy import text


def pause(listar=True):
    """
    pause a execução do programa até que o usuário pressione Enter.

    Args:
        listar (bool, opcional): Se True, imprime todos os movies antes de pauser.
                                 Padrão é True.
    """
    if listar:
        tb_movies.print_all()
    input("\nTecle Enter para continuar...")
    clear_screen()


def clear_screen():
    """
    Limpa a tela do console, imprimindo múltiplas quebras de linha.
    """
    print("\n" * 10)


# Inicializar o banco de dados
initialize_database()

# Inicializa o repositório de movies e atualiza a estrutura da tabela
tb_movies = movieRepository()
tb_movies.atualiza()

# USANDO SQL PURO
print("\nLISTANDO todos os movies como SQL puro...")
"""
ATENÇÃO!!
O que segue em relação ao uso de SQL PURO é apenas uma demonstração de 
recurso. Seu uso pode trazer problemas de compatibilidade entre bancos 
diferentes. O ideal é padronizar todas as consultas via ORM. 
"""
with get_connection() as conn:
    try:
        result = conn.execute(text("SELECT * FROM movies;"))
        for row in result:
            print(row)
    except Exception as e:
        print(f"Erro ao executar SQL puro: {e}")
pause(False)

# LISTA O CONTEÚDO DA TABELA
print("\nLISTANDO todos os movies...")
tb_movies.print_all()
pause(False)

# INSERT
print("\nINSERINDO um novo movie...")
tb_movies.insert({"titulo": "Matrix", "genero": "Ficção", "ano": 1999})
pause()

# UPDATE
print("\nATUALIZANDO o ano do movie Matrix...")
rows_updated = tb_movies.update(where={"titulo": "Matrix"}, with_={"ano": 2001})
if rows_updated:
    print(f"{rows_updated} movie(s) atualizado(s).")
pause()

# DELETE
print("\nDELETANDO o movie Matrix...")
tb_movies.delete(where={"titulo": "Matrix"})
pause()

# QUERY
print("\nCONSULTANDO movies do gênero 'Drama'...")
movies = tb_movies.get_by_field(where={"genero": "Drama"})
for movie in movies:
    print(movie)  # Agora os dicionários não terão `_sa_instance_state`
pause()
