from datetime import datetime
from bson import ObjectId
from typing import List, Optional

from app.models.booking_model import BookingCreate, BookingResponse, EventNested, VenueNested
from app.models.admin_model import AdminResponse
from app.models.user_model import UserResponse

from app.utils.exceptions import (
    UnauthorizedException,
    NotFoundException,
    BookingNotFoundException
)
from app.utils.sequence_utils import get_next_booking_id

from database.connection import db

class BookingService:
    def __init__(self):
        self.booking_collection = db["bookings"]
        self.event_collection = db["events"]
        self.venue_collection = db["venues"]


# ----------------- Get booking by ID (common) -----------------
    async def get_booking_by_id(self, booking_id: str) -> BookingResponse:
        booking = await self.booking_collection.find_one({"booking_id": booking_id})
        if not booking:
            raise BookingNotFoundException(f"Booking {booking_id} not found")

        # Convert ObjectId to string
        booking["_id"] = str(booking["_id"])

        # Fetch event and venue from booking
        event = booking.get("event")
        venue = booking.get("venue")

        return BookingResponse(
            id=booking["_id"],
            booking_date=booking["booking_date"],
            status=booking["status"],
            user_id=booking["user_id"],
            user_name=booking["user_name"],
            event_id=booking["event_id"],
            seats_booked=booking["seats_booked"],
            event=EventNested(**event) if event else None,
            venue=VenueNested(**venue) if venue else None
        )


# ---------- Create Booking (User only) ----------
    async def create_booking(self, booking: BookingCreate, current_user: UserResponse) -> BookingResponse:
    # Get event
        event = await self.event_collection.find_one({"event_id": booking.event_id})
        if not event or not event.get("is_approved", False):
            raise NotFoundException(f"Event {booking.event_id} not found or not approved")

    # Get all already reserved seats (approved + pending)
        reserved_cursor = self.booking_collection.find({
            "event_id": booking.event_id,
            "status": {"$in": ["pending", "approved"]}
    })
        reserved_seats = []
        async for r in reserved_cursor:
            reserved_seats.extend(r["seats_booked"])
        all_reserved_seats = set(reserved_seats)

    # Check requested seats
        for seat in booking.seats_booked:
            if seat in all_reserved_seats:
                raise UnauthorizedException(f"Seat {seat} is already reserved")

    # Generate booking ID
        booking_id = await get_next_booking_id()

    # Get venue info
        venue = await self.venue_collection.find_one({"venue_id": event["venue_id"]}) if event else None

    # Prepare embedded event and venue objects
        event_doc = {
            "id": str(event["_id"]),
            "event_id": event["event_id"],
            "title": event["title"],
            "type": event["type"],
            "venue_id": event["venue_id"],
            "total_seats": event["total_seats"],
            "booked_seats": booking.seats_booked,  # only this user's seats
            "city": event["city"],
            "is_approved": event["is_approved"],
            "available_seats": event["total_seats"] - len(all_reserved_seats.union(set(booking.seats_booked)))
    }

        venue_doc = {
            "id": str(venue["_id"]),
            "venue_id": venue["venue_id"],
            "name": venue["name"],
            "city": venue["city"],
            "location": venue["location"],
            "capacity": venue["capacity"],
            "type": venue["type"],
            "events": venue["events"]
    }   if venue else None

    # Insert booking with full event & venue info
        booking_doc = {
            "booking_id": booking_id,
            "user_id": current_user.user_id,
            "user_name": current_user.Full_name,
            "event_id": booking.event_id,
            "seats_booked": booking.seats_booked,
            "status": "pending",
            "booking_date": datetime.utcnow(),
            "event": event_doc,
            "venue": venue_doc
    }

        result = await self.booking_collection.insert_one(booking_doc)
        booking_doc["_id"] = str(result.inserted_id)

    # Return Pydantic response
        return BookingResponse(
            id=booking_doc["_id"],
            booking_date=booking_doc["booking_date"],
            status=booking_doc["status"],
            user_id=booking_doc["user_id"],
            user_name=booking_doc["user_name"],
            event_id=booking_doc["event_id"],
            seats_booked=booking_doc["seats_booked"],
            event=EventNested(**event_doc),
            venue=VenueNested(**venue_doc) if venue_doc else None
    )

# ---------- Get all bookings (admin only) ----------
    async def get_all_bookings_admin(self, current_admin: AdminResponse) -> list[BookingResponse]:
        if current_admin.role != "admin":
            raise UnauthorizedException("Only admins can view all bookings")

        bookings_list = []

        async for b in self.booking_collection.find({}):
        # Embed event and venue
            event_data = b.get("event", {})
            venue_data = b.get("venue", {})

            event_obj = EventNested(**event_data) if event_data else None
            venue_obj = VenueNested(**venue_data) if venue_data else None

        # Build the BookingResponse explicitly
            booking_obj = BookingResponse(
                id=str(b["_id"]),
                booking_date=b["booking_date"],
                status=b["status"],
                user_id=b["user_id"],
                user_name=b["user_name"],
                event_id=b["event_id"],
                seats_booked=b["seats_booked"],
                event=event_obj,
                venue=venue_obj
        )

            bookings_list.append(booking_obj)

        return bookings_list
    

# ---------- Get current user's bookings ----------
    async def get_user_bookings(self, current_user: UserResponse) -> List[BookingResponse]:
        bookings_list = []

        async for b in self.booking_collection.find({"user_id": current_user.user_id}):
            if not b:
                continue

            # Embed event and venue objects if available
            event_data = b.get("event", {})
            venue_data = b.get("venue", {})

            event_obj = EventNested(**event_data) if event_data else None
            venue_obj = VenueNested(**venue_data) if venue_data else None

            booking_obj = BookingResponse(
                id=str(b["_id"]),
                booking_date=b["booking_date"],
                status=b["status"],
                user_id=b["user_id"],
                user_name=b["user_name"],
                event_id=b["event_id"],
                seats_booked=b["seats_booked"],
                event=event_obj,
                venue=venue_obj
            )

            bookings_list.append(booking_obj)

        if not bookings_list:
            raise BookingNotFoundException("No bookings found for this user")

        return bookings_list
    

# ---------- Approve Booking (Admin Only) ----------
    async def approve_booking(self, booking_id: str, current_admin: AdminResponse) -> BookingResponse:
        if current_admin.role != "admin":
            raise UnauthorizedException("Only admins can approve bookings")

        booking = await self.booking_collection.find_one({"booking_id": booking_id})
        if not booking:
            raise BookingNotFoundException(f"Booking {booking_id} not found")

        if booking["status"] != "pending":
            raise UnauthorizedException("Booking already processed")

        # Update event booked seats
        event = await self.event_collection.find_one({"event_id": booking["event_id"]})
        if not event:
            raise NotFoundException(f"Event {booking['event_id']} not found")

        booked_seats_set = set(event.get("booked_seats", []))
        for seat in booking["seats_booked"]:
            if seat in booked_seats_set:
                raise UnauthorizedException(f"Seat {seat} already booked")
            booked_seats_set.add(seat)

        await self.event_collection.update_one(
            {"event_id": event["event_id"]},
            {"$set": {"booked_seats": list(booked_seats_set)}}
        )

        # Update booking status
        await self.booking_collection.update_one(
            {"booking_id": booking_id},
            {"$set": {"status": "approved"}}
        )

        return await self.get_booking_by_id(booking_id)

# ---------- Reject Booking (Admin only) ----------
    async def reject_booking(self, booking_id: str, current_admin: AdminResponse) -> BookingResponse:
        if current_admin.role != "admin":
            raise UnauthorizedException("Only admins can reject bookings")

        booking = await self.booking_collection.find_one({"booking_id": booking_id})
        if not booking:
            raise BookingNotFoundException(f"Booking {booking_id} not found")

        if booking["status"] != "pending":
            raise UnauthorizedException("Booking is already processed")

    # Rollback event seats
        event = await self.event_collection.find_one({"event_id": booking["event_id"]})
        if event:
            updated_booked_seats = [seat for seat in event["booked_seats"] if seat not in booking["seats_booked"]]
            available_seats = event["total_seats"] - len(updated_booked_seats)

        # Update event collection
        await self.event_collection.update_one(
            {"event_id": event["event_id"]},
            {"$set": {"booked_seats": updated_booked_seats}}
        )

        # Update booking embedded event
        booking["event"]["booked_seats"] = []
        booking["event"]["available_seats"] = available_seats

    # Update booking status
        await self.booking_collection.update_one(
        {"booking_id": booking_id},
        {"$set": {"status": "rejected", "event": booking["event"]}}
    )

        return await self.get_booking_by_id(booking_id)

# ---------- Cancel Booking (User Only) ----------
    async def cancel_booking(self, booking_id: str, current_user: UserResponse) -> BookingResponse:
        booking = await self.booking_collection.find_one({"booking_id": booking_id})
        if not booking:
            raise BookingNotFoundException(f"Booking {booking_id} not found")

        if booking["user_id"] != current_user.user_id:
            raise UnauthorizedException("You can only cancel your own bookings")

    # Rollback event seats if approved or pending
        event = await self.event_collection.find_one({"event_id": booking["event_id"]})
        if event:
            updated_booked_seats = [seat for seat in event["booked_seats"] if seat not in booking["seats_booked"]]
            available_seats = event["total_seats"] - len(updated_booked_seats)

        # Update event collection
        await self.event_collection.update_one(
            {"event_id": event["event_id"]},
            {"$set": {"booked_seats": updated_booked_seats}}
        )

        # Update booking embedded event
        booking["event"]["booked_seats"] = []
        booking["event"]["available_seats"] = available_seats

    # Update booking status
        await self.booking_collection.update_one(
        {"booking_id": booking_id},
        {"$set": {"status": "cancelled", "event": booking["event"]}}
    )

        return await self.get_booking_by_id(booking_id)