from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ---------- Venue Base ----------
class VenueBase(BaseModel):
    venue_id: Optional[str]
    name: str = Field(..., min_length=3, max_length=100)
    city: str
    location: str
    capacity: int = Field(..., ge=1)
    type: str

# ---------- Venue Create ----------
class VenueCreate(VenueBase):
    events: List[str] = []   

# ---------- Venue Update ----------
class VenueUpdate(BaseModel):
    venue_id: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = Field(None, ge=1)
    type: Optional[str] = None
    events: Optional[List[str]] = None

# ---------- Venue Response ----------
class VenueResponse(VenueBase):
    id: str
    venue_id: str
    events: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True