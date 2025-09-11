from fastapi import APIRouter, Depends,status
from typing import List

from app.services.booking_service import BookingService

from app.models.booking_model import BookingCreate, BookingResponse
from app.models.user_model import UserResponse
from app.models.admin_model import AdminResponse

from app.utils.exceptions import UnauthorizedException,HTTPException

from app.auth.auth_service import get_current_user, get_current_admin

router = APIRouter(prefix="/bookings", tags=["Bookings"])
booking_service = BookingService()

# ---------- User creates booking ----------
@router.post("/book-seats", response_model=BookingResponse)
async def create_booking(
    booking: BookingCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    return await booking_service.create_booking(booking, current_user)


# ---------- Get all bookings (Admin only) ----------
@router.get("/all-users-bookings", response_model=List[BookingResponse])
async def get_all_bookings(current_admin: AdminResponse = Depends(get_current_admin)):
    try:
        return await booking_service.get_all_bookings_admin(current_admin)
    except UnauthorizedException as e:
        # Returns 401 in Postman if a user token is used
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    

# ---------- Get logged-in user's bookings ----------
@router.get("/my-bookings", response_model=List[BookingResponse])
async def get_my_bookings(current_user: UserResponse = Depends(get_current_user)):
    return await booking_service.get_user_bookings(current_user)


# ---------- Approve booking (admin only) ----------
@router.put("/approve/{booking_id}", response_model=BookingResponse)
async def approve_booking(
    booking_id: str,
    current_admin: AdminResponse = Depends(get_current_admin)
):
    return await booking_service.approve_booking(booking_id, current_admin)

# ---------- Admin rejects a booking ----------
@router.put("/reject/{booking_id}", response_model=BookingResponse)
async def reject_booking(
    booking_id: str,
    current_admin: AdminResponse = Depends(get_current_admin)
):
    """
    Admin can reject a pending booking.
    Seats from the rejected booking will be rolled back to available.
    """
    return await booking_service.reject_booking(booking_id, current_admin)

# ---------- User cancels a booking ----------
@router.put("/cancel/{booking_id}", response_model=BookingResponse)
async def cancel_booking(
    booking_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    User can cancel their own booking.
    If booking was approved, seats are rolled back to available.
    """
    return await booking_service.cancel_booking(booking_id, current_user)
