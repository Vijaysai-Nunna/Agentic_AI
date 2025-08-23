from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EventBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str]
    date: datetime
    venue_id: str
    total_seats: int
    price: float

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    date: Optional[datetime]
    venue_id: Optional[str]
    total_seats: Optional[int]
    price: Optional[float]


class EventResponse(EventBase):
    id: str

    class Config:
        from_attributes = True
