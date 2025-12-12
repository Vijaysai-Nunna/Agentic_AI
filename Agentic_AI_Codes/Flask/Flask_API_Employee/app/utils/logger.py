import logging

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        file_handler = logging.FileHandler("employee_api.log")
        console_handler = logging.StreamHandler()
        detailed_format = '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(funcName)s() | [%(threadName)s] | %(message)s'

        formatter = logging.Formatter(detailed_format, datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        logger.setLevel(logging.INFO)
    return logger