from fastapi import Depends
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from bson import ObjectId

from database.connection import db

from database.connection import get_database

from app.models.admin_model import AdminResponse
from app.models.event_model import EventCreate, EventResponse,EventUpdate

from app.utils.sequence_utils import get_next_event_id
from app.utils.exceptions import UnauthorizedException,NotFoundException,EventNotFoundException
from app.utils.exceptions import (
    UnauthorizedException,
    NotFoundException,
    EventAlreadyExistsException,
)

from app.auth.auth_service import get_current_user

_event_service_instance = None

async def get_event_service(db=Depends(get_database)):
    global _event_service_instance
    if _event_service_instance is None:
        from app.services.event_service import EventService
        _event_service_instance = EventService(db)
    return _event_service_instance

class EventService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.event_collection = db["events"]
    

    # ---------- Utility: Serialize Event ----------
    def serialize_event(self, event: dict) -> EventResponse:
        return EventResponse(
            id=str(event["_id"]),
            event_id=event["event_id"],
            title=event["title"],
            type=event["type"],
            venue_id=event["venue_id"],
            city=event["city"],
            total_seats=event["total_seats"],
            booked_seats=event.get("booked_seats", []),
            is_approved=event.get("is_approved", False),
            created_at=event.get("created_at", datetime.utcnow())
        )

# ---------- Create Event (Admin only, manual event_id, unique title) ----------
    async def create_event(self, event: EventCreate, current_user) -> dict:
        # Only admins can create events
        if current_user.role != "admin":
            raise UnauthorizedException("Only admins can create events")

        # Check duplicate title
        if await self.collection.find_one({"title": event.title}):
            raise ValueError(f"Event with title '{event.title}' already exists")

        # If admin provided event_id, check duplicate
        if event.event_id:
            if await self.collection.find_one({"event_id": event.event_id}):
                raise ValueError(f"Event with event_id '{event.event_id}' already exists")
            event_id = event.event_id
        else:
            # Auto-generate next sequence ID
            event_id = await get_next_event_id()

        event_doc = {
            "event_id": event_id,
            "title": event.title,
            "type": event.type,
            "venue_id": event.venue_id,
            "city": event.city,
            "total_seats": event.total_seats,
            "booked_seats": [],
            "is_approved": True,
            "created_at": datetime.utcnow()
        }

        result = await self.collection.insert_one(event_doc)
        return {**event_doc, "id": str(result.inserted_id)}

#-------------------------Get event by id----------------------------------    
    async def get_event_by_id(self, event_id: str):
        event = await self.collection.find_one({"event_id": event_id})
        if not event:
            raise NotFoundException(f"Event with ID '{event_id}' not found")
        event["_id"] = str(event["_id"])
        return event


#------------------------------Get event by type--------------------------
    async def get_events_by_type(self, event_type: str):
        cursor = self.collection.find({"type": event_type})
        events = await cursor.to_list(length=None)
        if not events:
            raise NotFoundException(f"No events found for type '{event_type}'")
        for ev in events:
            ev["_id"] = str(ev["_id"])
        return events
    

     # ---------- Get All Events (Users & Admins) ----------
    async def get_all_events(self):
        events_cursor = self.event_collection.find({})
        events = []
        async for event in events_cursor:
            events.append(self.serialize_event(event))
        return events
    
#----------------------Update event(only admin)----------------------
    async def update_event(self, event_id: str, event_data: dict, current_admin: AdminResponse):
    # Only admin can update
        if not current_admin or current_admin.role != "admin":
            raise UnauthorizedException("Only admin can update events")

        # Find existing event
        event = await self.collection.find_one({"event_id": event_id})
        if not event:
            raise EventNotFoundException(f"Event {event_id} not found")

        update_dict = {}
        
        # Prevent duplicate title/type
        if event_data.get("title") or event_data.get("type"):
            query = {}
            if event_data.get("title"):
                query["title"] = event_data["title"]
            if event_data.get("type"):
                query["type"] = event_data["type"]
            query["_id"] = {"$ne": event["_id"]}  # exclude current event

            duplicate = await self.collection.find_one(query)
            if duplicate:
                raise EventAlreadyExistsException("Event with same title and type already exists")

        # Only update fields that are provided
        for field, value in event_data.items():
            if value is not None:
                update_dict[field] = value

        if not update_dict:
            raise ValueError("No new data provided to update")

        update_dict["updated_at"] = datetime.utcnow()

        await self.collection.update_one({"_id": event["_id"]}, {"$set": update_dict})

        updated_event = await self.collection.find_one({"_id": event["_id"]})
        updated_event["id"] = str(updated_event["_id"])
        return updated_event
    
# ---------------------- Delete event (only admin) ----------------------
    async def delete_event(self, event_id: str, current_admin) -> dict:
    # Only admin can delete
        if not current_admin or current_admin.role != "admin":
            raise UnauthorizedException("Only admin can delete events")

    # Find event
        event = await self.collection.find_one({"event_id": event_id})
        if not event:
            raise EventNotFoundException(f"Event {event_id} not found")

    # Delete event
        result = await self.collection.delete_one({"_id": event["_id"]})
        if result.deleted_count == 0:
            raise EventNotFoundException(f"Failed to delete event {event_id}")

        # Return deleted event details
        event["_id"] = str(event["_id"])  # Convert ObjectId for JSON serialization
        return {
        "message": f"Event {event_id} deleted successfully",
        "deleted_event": event
    }