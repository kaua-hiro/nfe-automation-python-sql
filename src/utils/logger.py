import logging
import os
from logging.handlers import TimedRotatingFileHandler

def setup_logger():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger("RoboEmpresaConfidencial")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    arquivo_handler = TimedRotatingFileHandler(
        filename='logs/robo_diario.log',
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    
    # Formato detalhado (Data - NÃ­vel - Mensagem)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    arquivo_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(arquivo_handler)
    logger.addHandler(console_handler)

    return logger
