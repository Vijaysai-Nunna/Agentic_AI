from pydantic import BaseModel, Field
from typing import Optional

class VenueBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    location: str
    capacity: int

class VenueCreate(VenueBase):
    pass

class VenueUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    capacity: Optional[int]

class VenueResponse(VenueBase):
    id: str

    class Config:
        from_attributes = True
