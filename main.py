from database import initialize_database, get_connection
from utils.populate import populate_database
from sqlalchemy import text

from repositories.movie_repository import MovieRepository
from repositories.genre_repository import GenreRepository
from repositories.movie_genre_repository import MovieGenreRepository
from repositories.actor_repository import ActorRepository

from Avaliacao.actor_crud import ActorCrud

import os

def pause(list_all=True):
    # Ignorar input se estiver rodando dentro de um container Docker
    if os.getenv("DOCKER_ENV") == "true":
        print("\n[Docker] Ignorando entrada do usuário.")
    else:
        input("\nPress Enter to continue...")
    clear_screen()


def clear_screen():
    """
    Clears the console screen by printing multiple line breaks.
    """
    print("*" * 90)
    print("\n" * 1)


# Initialize the database
initialize_database()

# Popula o banco de dados se necessário
# populate_database()  # Chama a função para popular as tabelas essenciai

ActorCrud()


# Initialize the movie repository and update the table structure
# tb_movies = MovieRepository()
# tb_genre = GenreRepository()
# tb_movies_genre = MovieGenreRepository()




# print(f"ID do ator: {id_ator}")



# EXIBE FILMES CADASTRADOS
# movies = tb_movies.list_movies_with_genres()
# print(f"{'Filme':<50} Gênero")
# print("-"*65)
# for movie in movies:
#     print(f"{movie['title']:<50} {movie['genres']}")

#
# # LIST TABLE CONTENT
# print("\nLISTING all movies...")
# tb_movies.print_all()
# pause(False)
#
# # EXIBE GENEROS CADASTRADOS
# print("\nLISTING all Genre...")
# tb_genre.print_all()
# pause(False)
#
#
#
# # EXIBE FILMES E GENEROS CADASTRADOS
# print("\nLISTING all Movie x Genre...")
# tb_movies_genre.print_all()
# pause(False)
#
#
#
#
#
#
#
# # USING RAW SQL
# print("\nLISTING all movies using raw SQL...")
# """
# WARNING!!
# The following example demonstrates the use of RAW SQL.
# Using raw SQL can lead to compatibility issues across different databases.
# It is recommended to use ORM-based queries instead.
# """
# with get_connection() as conn:
#     try:
#         result = conn.execute(text("SELECT * FROM movies;"))
#         for row in result:
#             print(row)
#     except Exception as e:
#         print(f"Error executing raw SQL: {e}")
# pause(False)
#
#
#
#
# print("\nLISTING all Genre...")
# tb_genre.print_all()
# pause(False)
#
#
#
# # INSERT
# print("\nINSERTING a new movie...")
# tb_movies.insert({"title":"Matrix", "year":1999, "duration":148, "classification_id":4, "rating":9}),
# pause()
#
#
# # UPDATE
# print("\nUPDATING the release year of 'Matrix'...")
# rows_updated = tb_movies.update(where={"title": "Matrix"}, with_={"year": 2001})
# if rows_updated:
#     print(f"{rows_updated} movie(s) updated.")
# pause()
#
#
# # DELETE
# print("\nDELETING the movie 'Matrix'...")
# tb_movies.delete(where={"title": "Matrix"})
# pause()
#
#
# # QUERY
# print("\nQUERYING movies of the 'Drama' genre...")
# movies = tb_movies.get_by_field(where={"genre": "Drama"})
# for movie in movies:
#     print(movie)  # Now the dictionaries will not contain `_sa_instance_state`
# pause()
