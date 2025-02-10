"""
main.py
Este módulo é o ponto de entrada da aplicação.
"""
from database import initialize_database
from utils.populate import populate_database
from Avaliacao.actor_crud import ActorCrud
from Avaliacao.director_crud import DirectorCrud
from Avaliacao.genre_crud import GenreCrud
from Avaliacao.classification_crud import ClassificationCrud
from Avaliacao.cinema_session_crud import CinemaSessionCrud
from Avaliacao.ticket_crud import TicketCrud
from Avaliacao.movie_crud import MovieCrud


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
        # populate_database()

        # Inicializa os CRUDs
        logging.info("Inicializando CRUDs...")
        ActorCrud()
        # DirectorCrud()
        # GenreCrud()
        # ClassificationCrud()
        # CinemaSessionCrud()
        # TicketCrud()
        # MovieCrud()

        logging.info("Fim dos Cruds.")
    except Exception as e:
        logging.error(f"Erro durante a execução: {e}")

if __name__ == "__main__":
    main()