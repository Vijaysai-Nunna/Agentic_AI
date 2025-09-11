from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ---------- Booking Base ----------
class BookingBase(BaseModel):
    event_id: str
    seats_booked: List[int] = Field(..., min_items=1)

# ---------- Booking Create ----------
class BookingCreate(BookingBase):
    pass  


# ---------- Event Nested in Booking ----------
class EventNested(BaseModel):
    id: str
    event_id: str
    title: str
    type: str
    venue_id: str
    total_seats: int
    booked_seats: List[int] = []
    city: str
    is_approved: bool
    available_seats: int

# ---------- Venue Nested in Booking ----------
class VenueNested(BaseModel):
    id: str
    venue_id: str
    name: str
    city: str
    location: str
    capacity: int
    type: str
    events: List[str] = []

# ---------- Booking Response ----------
class BookingResponse(BookingBase):
    id: str
    booking_date: datetime
    status: str = "pending"
    user_id: str
    user_name: str
    event: Optional[EventNested] = None
    venue: Optional[VenueNested] = None


    class Config:
        from_attributes = True
