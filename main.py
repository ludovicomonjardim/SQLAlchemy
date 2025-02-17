"""
main.py
Este módulo é o ponto de entrada da aplicação.
"""
from database import initialize_database
from utils.populate import populate_database
from manual_tests.actor_crud import ActorCrud
from manual_tests.director_crud import DirectorCrud
from manual_tests.genre_crud import GenreCrud
from manual_tests.classification_crud import ClassificationCrud
from manual_tests.cinema_session_crud import CinemaSessionCrud
from manual_tests.ticket_crud import TicketCrud
from manual_tests.movie_crud import MovieCrud


import logging
from utils.logging_config import setup_logger

# Configura o logger
setup_logger()

def main():
    try:
        # Inicializa o banco de dados
        logging.info("Inicializando banco de dados...")
        initialize_database()

        # Popula o banco de dados com dados iniciais
        # logging.info("Populando banco de dados...")
        populate_database()


        # Inicializa os CRUDs
        # logging.info("Inicializando CRUDs...")
        # ActorCrud()
        # DirectorCrud()
        # GenreCrud()
        # ClassificationCrud()
        # CinemaSessionCrud()
        # TicketCrud()
        MovieCrud()

        logging.info("Fim dos Cruds.")
    except Exception as e:
        logging.error(f"Erro durante a execução: {e}")

if __name__ == "__main__":
    main()