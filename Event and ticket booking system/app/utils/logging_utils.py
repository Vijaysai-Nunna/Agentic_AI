import logging
from config import LOG_LEVEL

# Configure root logger
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(), 
        logging.FileHandler("app.log", encoding="utf-8")  
    ]
)

logger = logging.getLogger("event_booking")

def get_logger(name: str = "event_booking") -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)
