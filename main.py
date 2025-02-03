from database import initialize_database, get_connection
from repositories.movie_repository import MovieRepository
from utils.populate import populate_database
from sqlalchemy import text
from time import sleep

import os

print(f'\nDOCKER_ENV: {os.getenv("DOCKER_ENV")}\n')
sleep(2)

def pause(list_all=True):
    """
    Pauses the program execution until the user presses Enter.

    Args:
        list_all (bool, optional): If True, prints all movies before pausing.
                                   Default is True.
    """
    if list_all:
        tb_movies.print_all()

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
populate_database()  # Chama a função para popular as tabelas essenciai

# Initialize the movie repository and update the table structure
tb_movies = MovieRepository()

movies = tb_movies.list_movies_with_genres()
print(f"{'Filme':<50} Gênero")
print("-"*65)
for movie in movies:
    print(f"{movie['title']:<50} {movie['genres']}")
    # print(f"{movie.title:<30} {movie.year:<5}")



# USING RAW SQL
print("\nLISTING all movies using raw SQL...")
"""
WARNING!!
The following example demonstrates the use of RAW SQL.
Using raw SQL can lead to compatibility issues across different databases.
It is recommended to use ORM-based queries instead.
"""
with get_connection() as conn:
    try:
        result = conn.execute(text("SELECT * FROM movies;"))
        for row in result:
            print(row)
    except Exception as e:
        print(f"Error executing raw SQL: {e}")
pause(False)


# LIST TABLE CONTENT
print("\nLISTING all movies...")
tb_movies.print_all()
pause(False)


# INSERT
print("\nINSERTING a new movie...")
tb_movies.insert({"title":"Matrix", "year":1999, "duration":148, "classification_id":4, "rating":9}),
pause()


# UPDATE
print("\nUPDATING the release year of 'Matrix'...")
rows_updated = tb_movies.update(where={"title": "Matrix"}, with_={"year": 2001})
if rows_updated:
    print(f"{rows_updated} movie(s) updated.")
pause()


# DELETE
print("\nDELETING the movie 'Matrix'...")
tb_movies.delete(where={"title": "Matrix"})
pause()


# QUERY
print("\nQUERYING movies of the 'Drama' genre...")
movies = tb_movies.get_by_field(where={"genre": "Drama"})
for movie in movies:
    print(movie)  # Now the dictionaries will not contain `_sa_instance_state`
pause()
