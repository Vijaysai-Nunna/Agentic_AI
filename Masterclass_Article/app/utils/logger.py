import logging
import os

# Make sure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure the logger
logging.basicConfig(
    filename="logs/logs_collection.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("MongoDBLogger")
