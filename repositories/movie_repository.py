from utils.session import session_manager
from utils.migration import atualizar_tabela
from sqlalchemy import select
from models.movie import Movie
from models.genre import Genre

from models.movie_genre import MovieGenre

from repositories.movie_actor_repository import MovieActorRepository
from repositories.movie_director_repository import MovieDirectorRepository
from repositories.movie_genre_repository import MovieGenreRepository
from repositories.cinema_session_repository import CinemaSessionRepository
from repositories.ticket_repository import TicketRepository


import logging


class MovieRepository:
    """
    Repositório responsável pelas operações de banco de dados para a entidade movie.

    Métodos incluem inserção, atualização, deleção e busca de registros na tabela 'movies'.
    """

    @staticmethod
    def update_structure():
        """
        Atualiza a estrutura da tabela 'movies', garantindo que a estrutura seja substituída corretamente.

        Este método verifica a estrutura atual da tabela e adiciona colunas ausentes conforme o modelo definido.
        """
        try:
            atualizar_tabela(Movie)
            print("Atualização da tabela 'movies' concluída com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar a tabela 'movies': {e}")

    @staticmethod
    @session_manager
    def insert(data, session):
        """
        Insere um ou vários movies no banco de dados.

        Args:
            data (dict | list[dict]): Um dicionário representando um movie ou uma lista de dicionários para inserção em massa.
            session (Session): Sessão ativa do SQLAlchemy.

        Returns:
            bool: True se a inserção for bem-sucedida, False caso contrário.
        """
        try:
            if isinstance(data, list):
                movies = [Movie(**movie_data) for movie_data in data]
                session.bulk_save_objects(movies)
                print(f"{len(movies)} filmes inseridos com sucesso!")
            else:
                movie = Movie(**data)
                session.add(movie)
                print(f"Filme '{movie.title}' inserido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir filme(s): {e}")
            return False

    @staticmethod
    @session_manager
    def update(where, with_, session):
        """
        Atualiza registros na tabela 'movies' com base nos critérios fornecidos.

        Args:
            where (dict): Condições para localizar os registros a serem atualizados (exemplo: {"title": "Matrix"}).
            with_ (dict): Valores a serem atribuídos aos registros encontrados (exemplo: {"year": 2001}).
            session (Session): Sessão ativa do SQLAlchemy.

        Returns:
            int: Número de registros modificados.
        """
        try:
            result = session.query(Movie).filter_by(**where).update(with_, synchronize_session=False)
            session.commit()
            print(f"{result} filme(s) atualizado(s) com sucesso.")
            return result
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar filme(s): {e}")
            return 0

    @staticmethod
    @session_manager
    def delete(where, session):
        try:
            # Buscar o filme a ser excluído
            movie = session.query(Movie).filter_by(**where).first()
            if not movie:
                print("Nenhum filme encontrado para deleção.")
                return 0

            # Criar instâncias dos repositórios
            tb_movie_actor = MovieActorRepository()
            tb_movie_director = MovieDirectorRepository()
            tb_movie_genre = MovieGenreRepository()
            tb_cinema_session = CinemaSessionRepository()
            tb_ticket = TicketRepository()

            # Remover associações de atores, diretores e gêneros do filme
            tb_movie_actor.delete(where={"movie_id": movie.id})
            tb_movie_director.delete(where={"movie_id": movie.id})
            tb_movie_genre.delete(where={"movie_id": movie.id})

            # Remover sessões de cinema associadas ao filme
            cinema_sessions = session.query(CinemaSession).filter_by(movie_id=movie.id).all()
            for session_ in cinema_sessions:
                tb_ticket.delete(where={"cinema_session_id": session_.id})

            tb_cinema_session.delete(where={"movie_id": movie.id})

            # Agora podemos excluir o filme
            session.delete(movie)
            print(f"Filme '{movie.title}' e todas as suas associações foram removidos com sucesso.")
            return 1

        except Exception as e:
            session.rollback()
            print(f"Erro ao deletar filme: {e}")
            return 0

    @staticmethod
    @session_manager
    def get_by_field(session, where, fields=None):
        """
        Busca movies com base nos critérios especificados e retorna os campos solicitados.

        Args:
            session (Session): Sessão ativa do SQLAlchemy.
            where (dict): Critérios de filtro para a consulta (exemplo: {"ano": 1999, "genero": "Ficção"}).
            fields (list[str], opcional): Lista de colunas a serem retornadas (exemplo: ["titulo", "ano"]).
                                          Se None, retorna todos os campos.

        Returns:
            list[dict]: Lista de dicionários representando os movies encontrados.
        """
        try:
            query = session.query(Movie).filter_by(**where)

            if fields:
                query = query.with_entities(*[getattr(Movie, field) for field in fields])
                movies = query.all()
                return [dict(zip(fields, movie)) for movie in movies]
            else:
                movies = query.all()
                return [
                    {key: value for key, value in movie.__dict__.items() if key != "_sa_instance_state"}
                    for movie in movies
                ]  # Remove `_sa_instance_state` antes de retornar
        except Exception as e:
            print(f"Erro ao buscar filmes: {e}")
            return []

    @staticmethod
    @session_manager
    def get_by_titulo(titulo, session):
        """
        Busca um movie pelo título.

        Args:
            titulo (str): Nome do movie a ser buscado.
            session (Session): Sessão ativa do SQLAlchemy.

        Returns:
            Movie | None: O objeto movie encontrado ou None se não existir.
        """
        movie = session.query(Movie).filter(Movie.title == titulo).first()
        if movie:
            session.expunge(movie)  # Remove a ligação do objeto com a sessão para evitar efeitos colaterais
        return movie

    @staticmethod
    @session_manager
    def print_all(session):
        """
        Imprime todos os movies da tabela 'movies' em formato tabular.

        Args:
            session (Session): Sessão ativa do SQLAlchemy.
        """
        movies = session.query(Movie).all()
        if movies:
            print()
            print("-" * 51)
            print(f"{'Título':<30} {'Ano':<5}")
            print("-" * 51)
            for movie in movies:
                print(f"{movie.title:<30} {movie.year:<5}")
        else:
            print("Nenhum filme encontrado na tabela.")

    @staticmethod
    @session_manager
    def list_movies_with_genres(session):
        """
        Retorna uma lista de filmes com seus respectivos gêneros.

        Args:
            session (Session): Sessão ativa do SQLAlchemy.

        Returns:
            list[dict]: Lista de dicionários contendo 'title' e 'genres'.
        """
        stmt = (
            select(Movie.title, Genre.name)
            .join(MovieGenre, Movie.id == MovieGenre.movie_id)
            .join(Genre, MovieGenre.genre_id == Genre.id)
            .order_by(Movie.title)
        )
        results = session.execute(stmt).all()

        movies_dict = {}
        for title, genre in results:
            if title in movies_dict:
                movies_dict[title].append(genre)
            else:
                movies_dict[title] = genre

        movies_list = []
        for title, genres in movies_dict.items():
            movie_entry = {
                "title": title,
                "genres": genres
            }
            movies_list.append(movie_entry)
        return movies_list

        # return [{"title": title, "genres": genres} for title, genres in movies_dict.items()]

# Configuração do logging para capturar erros
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
