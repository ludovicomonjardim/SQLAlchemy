from database import initialize_database, conn
from repositories.filme_repository import FilmeRepository
from sqlalchemy import text

def pausa(listar=True):
    if listar:
        tb_filmes.print_all()
    input("\nTecle Enter para continuar...")
    print("\n" * 15)



# Inicializar o banco de dados
initialize_database()

tb_filmes = FilmeRepository()


# USANDO SQL PURO
print("\nLISTANDO todos os filmes como SQL puro...")
result = conn.execute(text("SELECT * FROM filmes;"))
for row in result:
        print(row)  # Cada linha será uma tupla representando os dados
pausa(False)


# LISTA O CONTEÚDO DA TABELA
print("\nLISTANDO todos os filmes...")
tb_filmes.print_all()
pausa(False)


# INSERT
print("\nINSERINDO um novo filme...")
tb_filmes.insert({"titulo": "Matrix", "genero": "Ficção", "ano": 999})
pausa()

# UPDATE
print("\nATUALIZANDO o ano do filme Matrix...")
rows_updated = tb_filmes.update(where={"titulo": "Matrix"}, with_={"ano": 2001})
if rows_updated:
    print(f"{rows_updated} filme(s) atualizado(s).")
pausa()

#  DETELE
print("\nDELETANDO o filme Matrix...")
tb_filmes.delete(where={"titulo": "Matrix"})
pausa()



#
# QUERY
print("\nQUERY ano = 1999...")
filmes = tb_filmes.get_by_field(where={"genero": "Drama"})
for filme in filmes:
    print(filme)  # Agora os dicionários não terão `_sa_instance_state`


pausa()
