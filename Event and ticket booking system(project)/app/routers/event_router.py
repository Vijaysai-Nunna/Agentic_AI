from fastapi import APIRouter, Depends, HTTPException
from typing import List

from database.connection import db
from database.connection import get_database

from app.models.event_model import EventCreate, EventResponse,EventUpdate
from app.models.admin_model import AdminResponse

from app.services.event_service import EventService
from app.services.event_service import get_event_service

from app.auth.auth_service import get_current_user,get_current_admin

from app.utils.exceptions import UnauthorizedException,NotFoundException,EventNotFoundException,EventAlreadyExistsException

router = APIRouter(prefix="/events", tags=["Events"])
event_service = EventService(db)

# ---------- Create Event ----------
@router.post("/Create-event", response_model=EventResponse)
async def create_event(event: EventCreate, current_user=Depends(get_current_user)):
    try:
        return await event_service.create_event(event, current_user)
    except UnauthorizedException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

#-------------Get event by id--------------
@router.get("/by-id/{event_id}")
async def get_event_by_id(event_id: str, db=Depends(get_database)):
    service = EventService(db)
    return await service.get_event_by_id(event_id)

#-------------Get event by type---------------
@router.get("/by-type/{event_type}")
async def get_events_by_type(event_type: str, db=Depends(get_database)):
    service = EventService(db)
    return await service.get_events_by_type(event_type)


# ---------- Get All Events (Users & Admins) ----------
@router.get("/all-events", response_model=List[EventResponse])
async def get_all_events(current_user=Depends(get_current_user)):
    return await event_service.get_all_events()

# -------- Update Event --------
@router.put("/update/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: str,
    event_data: EventUpdate,
    event_service: EventService = Depends(get_event_service),
    current_admin: dict = Depends(get_current_admin),
):
    return await event_service.update_event(event_id, event_data.dict(exclude_unset=True), current_admin)


# ---------------- Delete Event ----------------
@router.delete("/delete/{event_id}")
async def delete_event(
    event_id: str,
    current_admin: AdminResponse = Depends(get_current_admin),
    event_service: EventService = Depends(get_event_service)
):
    return await event_service.delete_event(event_id, current_admin)