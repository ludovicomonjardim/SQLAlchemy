from datetime import date, time, datetime, timezone  # Importar timezone corretamente

from database import Session, initialize_database
from models.actor import Actor
from models.classification import Classification
from models.director import Director
from models.genre import Genre
from models.movie import Movie
from models.movie_actor import MovieActor
from models.movie_director import MovieDirector
from models.movie_genre import MovieGenre
from models.cinema_session import CinemaSession
from models.ticket import Ticket
from datetime import date, time, datetime

def populate_database():
    initialize_database()  # Garantir que as tabelas estão criadas

    with Session() as session:
        try:
            # Inserindo classificações
            classifications = [
                Classification(name="Livre", description="Para todos os públicos", min_age=0),
                Classification(name="10 anos", description="Não recomendado para menores de 10 anos", min_age=10),
                Classification(name="12 anos", description="Não recomendado para menores de 12 anos", min_age=12),
                Classification(name="14 anos", description="Não recomendado para menores de 14 anos", min_age=14),
                Classification(name="16 anos", description="Não recomendado para menores de 16 anos", min_age=16),
                Classification(name="18 anos", description="Não recomendado para menores de 18 anos", min_age=18),
            ]
            session.bulk_save_objects(classifications)

            # Inserindo gêneros
            genres = [
                Genre(name="Ação"),
                Genre(name="Comédia"),
                Genre(name="Drama"),
                Genre(name="Ficção Científica"),
                Genre(name="Terror"),
            ]
            session.bulk_save_objects(genres)

            # Inserindo diretores
            directors = [
                Director(name="Steven Spielberg"),
                Director(name="Christopher Nolan"),
                Director(name="Quentin Tarantino"),
                Director(name="Martin Scorsese"),
            ]
            session.bulk_save_objects(directors)

            # Inserindo atores
            actors = [
                Actor(name="Leonardo DiCaprio"),
                Actor(name="Brad Pitt"),
                Actor(name="Tom Hanks"),
                Actor(name="Natalie Portman"),
                Actor(name="Scarlett Johansson"),
            ]
            session.bulk_save_objects(actors)

            # Inserindo filmes
            movies = [
                Movie(title="Inception", year=2010, duration=148, classification_id=4, rating=9),
                Movie(title="Pulp Fiction", year=1994, duration=154, classification_id=5, rating=8),
                Movie(title="O Resgate do Soldado Ryan", year=1998, duration=169, classification_id=5, rating=9),
                Movie(title="Interestelar", year=2014, duration=169, classification_id=4, rating=9),
            ]
            session.bulk_save_objects(movies)
            session.commit()  # GARANTE que os filmes foram salvos antes de usar seus IDs

            # Consultar os IDs dos filmes e gêneros para garantir que existem
            movies_dict = {movie.title: movie.id for movie in session.query(Movie).all()}
            genres_dict = {genre.name: genre.id for genre in session.query(Genre).all()}

            # Relacionando filmes a gêneros
            movie_genres = [
                MovieGenre(movie_id=movies_dict["Inception"], genre_id=genres_dict["Ficção Científica"]),
                MovieGenre(movie_id=movies_dict["Pulp Fiction"], genre_id=genres_dict["Drama"]),
                MovieGenre(movie_id=movies_dict["O Resgate do Soldado Ryan"], genre_id=genres_dict["Ação"]),
                MovieGenre(movie_id=movies_dict["Interestelar"], genre_id=genres_dict["Ficção Científica"]),
            ]
            session.bulk_save_objects(movie_genres)

            # Relacionando filmes a diretores
            directors_dict = {director.name: director.id for director in session.query(Director).all()}
            movie_directors = [
                MovieDirector(movie_id=movies_dict["Inception"], director_id=directors_dict["Christopher Nolan"]),
                MovieDirector(movie_id=movies_dict["Pulp Fiction"], director_id=directors_dict["Quentin Tarantino"]),
                MovieDirector(movie_id=movies_dict["O Resgate do Soldado Ryan"], director_id=directors_dict["Steven Spielberg"]),
                MovieDirector(movie_id=movies_dict["Interestelar"], director_id=directors_dict["Christopher Nolan"]),
            ]
            session.bulk_save_objects(movie_directors)

            # Relacionando filmes a atores
            actors_dict = {actor.name: actor.id for actor in session.query(Actor).all()}
            movie_actors = [
                MovieActor(movie_id=movies_dict["Inception"], actor_id=actors_dict["Leonardo DiCaprio"], role="Dom Cobb"),
                MovieActor(movie_id=movies_dict["Pulp Fiction"], actor_id=actors_dict["Brad Pitt"], role="Vincent Vega"),
                MovieActor(movie_id=movies_dict["O Resgate do Soldado Ryan"], actor_id=actors_dict["Tom Hanks"], role="Capitão Miller"),
                MovieActor(movie_id=movies_dict["Interestelar"], actor_id=actors_dict["Natalie Portman"], role="Brand"),
            ]
            session.bulk_save_objects(movie_actors)

            # Criando sessões de cinema
            cinema_sessions = [
                CinemaSession(movie_id=movies_dict["Inception"], date=date(2025, 1, 10), time=time(19, 30), room="Sala 1", capacity=100, price=25.00),
                CinemaSession(movie_id=movies_dict["Pulp Fiction"], date=date(2025, 1, 11), time=time(20, 00), room="Sala 2", capacity=80, price=22.50),
                CinemaSession(movie_id=movies_dict["O Resgate do Soldado Ryan"], date=date(2025, 1, 12), time=time(21, 00), room="Sala 3", capacity=120, price=27.00),
            ]
            session.bulk_save_objects(cinema_sessions)
            session.commit()  # Confirma as inserções

            # Criando ingressos
            tickets = [
                Ticket(cinema_session_id=1, customer="João da Silva",
                       purchase_date=datetime(2025, 1, 5, 15, 0, tzinfo=timezone.utc)),
                Ticket(cinema_session_id=2, customer="Maria Oliveira",
                       purchase_date=datetime(2025, 1, 6, 18, 30, tzinfo=timezone.utc)),
                Ticket(cinema_session_id=3, customer="Carlos Souza",
                       purchase_date=datetime(2025, 1, 7, 20, 45, tzinfo=timezone.utc)),
            ]
            session.bulk_save_objects(tickets)
            session.commit()

            print("Banco de dados populado com sucesso!")

        except Exception as e:
            session.rollback()
            print(f"Erro ao popular banco de dados: {e}")

if __name__ == "__main__":
    populate_database()
