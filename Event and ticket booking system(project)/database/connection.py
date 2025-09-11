from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, DATABASE_NAME
from app.utils.logging_utils import get_logger

logger = get_logger(__name__)

# MongoDB client initialization
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]

async def get_database():
    """
    Provides the database instance for dependency injection.
    """
    try:
        logger.info(f"Connecting to MongoDB at {MONGODB_URL}, using DB: {DATABASE_NAME}")
        return db
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise e