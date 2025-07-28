import logging
import os

# Make sure logs directory exists
os.makedirs("logs", exist_ok=True)

# # Configure the logger
# logging.basicConfig(
#     filename="logs/users.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )
def setup_logger():
    """
    Setup logger for the application.
    This function can be called at the start of the application to initialize logging.
    """
    logger = logging.getLogger("user_logger")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler("logs/users.log")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

