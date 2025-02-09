import logging
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler
import os

def setup_logger(log_level="DEBUG", log_file=None):
    """
    Configura o logger com formatação colorida e opções adicionais.
    :param log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    :param log_file: Caminho para o arquivo de log (opcional).
    """
    # Define o nível de log
    level = getattr(logging, log_level.upper(), logging.DEBUG)

    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove handlers existentes
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Formato com cores
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(blue)s %(module)s:%(funcName)s %(lineno)d%(reset)s - %(white)s%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para arquivo (opcional)
    if log_file:
        # Cria o diretório se ele não existir
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Rotaciona logs para evitar arquivos muito grandes
        file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)  # 10MB por arquivo, mantém 5 backups
        file_formatter = logging.Formatter(
            "%(levelname)-8s %(asctime)s %(module)s:%(funcName)s %(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)