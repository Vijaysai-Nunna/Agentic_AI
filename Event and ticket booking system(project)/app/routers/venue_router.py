from fastapi import APIRouter, Depends,Body
from typing import List

from app.services.venue_service import VenueService

from app.models.venue_model import VenueCreate, VenueUpdate
from app.models.admin_model import AdminResponse
from app.models.user_model import UserResponse

from app.auth.auth_service import get_current_admin, get_current_user


router = APIRouter(prefix="/venues", tags=["Venues"])

venue_service = VenueService()

# ---------- Create Venue (Admin only) ----------
@router.post("/create-venue", response_model=dict)
async def create_venue(
    venue: VenueCreate,
    current_admin: AdminResponse = Depends(get_current_admin)
):
    return await venue_service.create_venue(venue, current_admin)


# ------------------------- Get venue by ID -------------------------
@router.get("/get/{venue_id}", response_model=dict)
async def get_venue_by_id(venue_id: str):
    return await venue_service.get_venue_by_id(venue_id)

# ------------------------- Get venues by type -------------------------
@router.get("/type/{venue_type}", response_model=List[dict])
async def get_venues_by_type(venue_type: str):
    return await venue_service.get_venues_by_type(venue_type)

# ------------------------- Get all venues -------------------------
@router.get("/all-venues", response_model=List[dict])
async def get_all_venues():
    return await venue_service.get_all_venues()

# ------------------------- Update venue (Admin only) -------------------------
@router.put("/update/{venue_id}", response_model=dict)
async def update_venue(
    venue_id: str,
    venue_update: VenueUpdate = Body(...),
    current_admin: AdminResponse = Depends(get_current_admin)
):
    return await venue_service.update_venue(venue_id, venue_update.dict(exclude_unset=True), current_admin)

# ------------------------- Delete venue (Admin only) -------------------------
@router.delete("/delete/{venue_id}", response_model=dict)
async def delete_venue(
    venue_id: str,
    current_admin: AdminResponse = Depends(get_current_admin)
):
    return await venue_service.delete_venue(venue_id, current_admin)