import logging


# Настройка уровня и файла логирования
def my_logs():
    logger = logging.getLogger(__name__)

    logging.basicConfig(filename='weather_logs.txt', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    return logger
