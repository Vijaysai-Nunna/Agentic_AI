import json
from database.collections import events_collection, venues_collection
from app.utils.logging_utils import get_logger

logger = get_logger(__name__)

async def init_db():
    """
    Initialize database with seed data (events & venues).
    """
    try:
        # Load sample events
        with open("Json_files/event.json", "r") as f:
            events_data = json.load(f)
        if events_data:
            await events_collection.insert_many(events_data)
            logger.info("Seeded events collection successfully")

        # Load sample venues
        with open("Json_files/venue.json", "r") as f:
            venues_data = json.load(f)
        if venues_data:
            await venues_collection.insert_many(venues_data)
            logger.info("Seeded venues collection successfully")

    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")