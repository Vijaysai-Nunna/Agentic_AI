from database.connection import db

async def get_next_sequence_id(entity: str, prefix: str) -> str:
    """
    Generate a sequential ID for a given entity.
    Example: get_next_sequence_id("user_id", "USR") -> USR001
    """
    counters = db["counters"]

    result = await counters.find_one_and_update(
        {"_id": entity},
        {"$inc": {"sequence_value": 1}},
        return_document=True,   
        upsert=True
    )

    return f"{prefix}{result['sequence_value']:03d}"


# Convenience wrappers
async def get_next_user_id() -> str:
    return await get_next_sequence_id("user_id", "USR")


async def get_next_admin_id() -> str:
    return await get_next_sequence_id("admin_id", "ADM")


async def get_next_event_id() -> str:
    return await get_next_sequence_id("event_id", "EVT")


async def get_next_venue_id() -> str:
    return await get_next_sequence_id("venue_id", "VEN")


async def get_next_booking_id() -> str:
    return await get_next_sequence_id("booking_id", "BKG")
