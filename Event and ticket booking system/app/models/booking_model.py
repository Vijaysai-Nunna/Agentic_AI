from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime

class BookingBase(BaseModel):
    user_id: str
    event_id: str
    seats_booked: List[int]
    booking_date: datetime = Field(default_factory=datetime.utcnow) 
    status: Literal["pending", "approved", "rejected", "cancelled"] = "pending" 

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    seats_booked: List[int]
    status: str

class BookingResponse(BookingBase):
    id: str

    class Config:
        from_attributes = True
