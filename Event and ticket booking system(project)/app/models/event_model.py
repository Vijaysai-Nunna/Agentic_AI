from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ---------- Event Base ----------
class EventBase(BaseModel):
    event_id: Optional[str]
    title: str = Field(..., min_length=3, max_length=100)
    type: str
    venue_id: str
    city: str
    total_seats: int = Field(..., ge=1)

# ---------- Event Create ----------
class EventCreate(EventBase):
    pass

# ---------- Event Update ----------
class EventUpdate(BaseModel):
    event_id: Optional[str]=None
    title: Optional[str]=None
    type: Optional[str]=None
    venue_id: Optional[str]=None
    city: Optional[str]=None
    total_seats: Optional[int] = Field(None, ge=1)
    is_approved: Optional[bool]=None

# ---------- Event Response ----------
class EventResponse(EventBase):
    id: str
    event_id: str
    booked_seats: List[int] = []
    is_approved: bool = False
    created_at: datetime

    class Config:
        from_attributes = True