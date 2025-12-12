import logging
from logging.handlers import RotatingFileHandler  


def get_logger(name):

    logger = logging.getLogger(name)

    #set the minimum log level to INFO 
    logger.setLevel(logging.INFO)

    #prevent adding handlers multiple times
    if not logger.handlers :

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s")


        file_handlers = RotatingFileHandler(
            "prompt_chain.log", maxBytes = 100_00_00 ,
            backupCount =10,
            encoding = 'utf-8'
        )

        file_handlers.setFormatter(formatter)


        #attach both handlers to the logger
        logger.addHandler(file_handlers)

    return logger