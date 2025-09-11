from bson import ObjectId
from datetime import datetime

from app.models.venue_model import VenueCreate, VenueUpdate, VenueResponse
from app.models.admin_model import AdminResponse

from app.utils.sequence_utils import get_next_venue_id
from app.utils.exceptions import UnauthorizedException, VenueNotFoundException, VenueAlreadyExistsException

from database.connection import db

class VenueService:
    def __init__(self):
        self.collection = db["venues"]

# ---------- Create Venue (Admin only, sequence ID) ----------
    async def create_venue(self, venue: VenueCreate, current_admin: AdminResponse):
        if not current_admin or current_admin.role != "admin":
            raise UnauthorizedException("Only admins can create venues")

        # Prevent duplicate name
        if await self.collection.find_one({"name": venue.name}):
            raise VenueAlreadyExistsException(f"Venue with name '{venue.name}' already exists")

        # Venue ID (manual or auto)
        if venue.venue_id:
            if await self.collection.find_one({"venue_id": venue.venue_id}):
                raise VenueAlreadyExistsException(f"Venue with ID '{venue.venue_id}' already exists")
            venue_id = venue.venue_id
        else:
            venue_id = await get_next_venue_id()

        venue_doc = {
            "venue_id": venue_id,
            "name": venue.name,
            "city": venue.city,
            "location": venue.location,
            "capacity": venue.capacity,
            "type": venue.type,
            "events": venue.events or [],
            "created_at": datetime.utcnow()
        }

        result = await self.collection.insert_one(venue_doc)
        venue_doc["_id"] = str(result.inserted_id)   # convert ObjectId
        return venue_doc
    

# ------------------------- Get venue by id -------------------------
    async def get_venue_by_id(self, venue_id: str):
        venue = await self.collection.find_one({"venue_id": venue_id})
        if not venue:
            raise VenueNotFoundException(f"Venue with ID '{venue_id}' not found")
        venue["_id"] = str(venue["_id"])
        return venue

# ------------------------- Get venues by type -------------------------
    async def get_venues_by_type(self, venue_type: str):
        cursor = self.collection.find({"type": venue_type})
        venues = await cursor.to_list(length=None)
        if not venues:
            raise VenueNotFoundException(f"No venues found for type '{venue_type}'")
        for v in venues:
            v["_id"] = str(v["_id"])
        return venues

# ------------------------- Get all venues -------------------------
    async def get_all_venues(self):
        cursor = self.collection.find({})
        venues = await cursor.to_list(length=None)
        for v in venues:
            v["_id"] = str(v["_id"])
        return venues

# ------------------------- Update venue (only admin) -------------------------
    async def update_venue(self, venue_id: str, venue_data: dict, current_admin: AdminResponse):
        if not current_admin or current_admin.role != "admin":
            raise UnauthorizedException("Only admin can update venues")

        # Find existing venue
        venue = await self.collection.find_one({"venue_id": venue_id})
        if not venue:
            raise VenueNotFoundException(f"Venue {venue_id} not found")

        update_dict = {}

        # Prevent duplicate name
        if venue_data.get("name"):
            duplicate = await self.collection.find_one({
                "name": venue_data["name"],
                "_id": {"$ne": venue["_id"]}
            })
            if duplicate:
                raise VenueAlreadyExistsException(f"Venue with name '{venue_data['name']}' already exists")

        # Only update provided fields
        for field, value in venue_data.items():
            if value is not None:
                update_dict[field] = value

        if not update_dict:
            raise ValueError("No new data provided to update")

        update_dict["updated_at"] = datetime.utcnow()

        await self.collection.update_one({"_id": venue["_id"]}, {"$set": update_dict})

        updated_venue = await self.collection.find_one({"_id": venue["_id"]})
        updated_venue["_id"] = str(updated_venue["_id"])   # convert ObjectId
        return updated_venue

# ------------------------- Delete venue (only admin) -------------------------
    async def delete_venue(self, venue_id: str, current_admin) -> dict:
        if not current_admin or current_admin.role != "admin":
            raise UnauthorizedException("Only admin can delete venues")

        # Find venue
        venue = await self.collection.find_one({"venue_id": venue_id})
        if not venue:
            raise VenueNotFoundException(f"Venue {venue_id} not found")

        # Delete venue
        result = await self.collection.delete_one({"_id": venue["_id"]})
        if result.deleted_count == 0:
            raise VenueNotFoundException(f"Failed to delete venue {venue_id}")

        venue["_id"] = str(venue["_id"])
        return {
            "message": f"Venue {venue_id} deleted successfully",
            "deleted_venue": venue
        }