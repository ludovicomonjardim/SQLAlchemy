import logging
from utils.logging_config import setup_logger
from database import initialize_database
from utils.populate import populate_database
from Avaliacao.actor_crud import ActorCrud

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

        logging.info("Aplicação inicializada com sucesso!")
    except Exception as e:
        logging.error(f"Erro durante a execução: {e}")

if __name__ == "__main__":
    main()