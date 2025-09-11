from fastapi import APIRouter, Depends, HTTPException

from typing import List

from database.connection import db
from database.collections import users_collection

from app.models.admin_model import AdminCreate, AdminLogin, AdminResponse,AdminUpdate

from app.auth.auth_service import get_current_user
from app.auth.auth_service import get_current_admin, oauth2_scheme

from app.services.admin_service import AdminService

from app.utils.exceptions import (
    UserAlreadyExistsException,
    PasswordMismatchException,
    InvalidCredentialsException,
    UnauthorizedException,
    AdminAlreadyExistsException,
    AdminNotFoundException
)

router = APIRouter(prefix="/admins", tags=["Admins"])
admin_service = AdminService(db)


#----------------------Register Admin---------------------
@router.post("/register", response_model=AdminResponse)
async def register_admin(admin: AdminCreate, current_user: AdminResponse = Depends(get_current_user)):
    try:
        return await admin_service.register_admin(admin, current_user)
    except PasswordMismatchException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AdminAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except UnauthorizedException as e:
        raise HTTPException(status_code=403, detail=str(e))

#-------------------------------------Login Admin--------------------------
@router.post("/login")
async def login_admin(login: AdminLogin):
    try:
        return await admin_service.login_admin(login)
    except AdminNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=str(e))    

# ---------------- Get Current Admin ----------------
@router.get("/me")
async def get_admin_info(current_user=Depends(get_current_user)):
    try:
        return await admin_service.get_current_admin(current_user)
    except UnauthorizedException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except AdminNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

# ---------------- Get All Users ----------------
@router.get("/all-users")
async def get_all_users(current_user=Depends(get_current_user)):
    try:
        return await admin_service.get_all_users(current_user)
    except UnauthorizedException as e:
        raise HTTPException(status_code=403, detail=str(e))
    
#-------------------Get All Admins--------------------
@router.get("/all-admins", response_model=List[AdminResponse])
async def get_all_admins(current_admin: AdminResponse = Depends(get_current_user)):
    try:
        return await admin_service.get_all_admins(current_admin)
    except UnauthorizedException as e:
        raise HTTPException(status_code=403, detail=str(e))


#-----------------------------Update Admin---------------------
@router.put("/update-admin", response_model=AdminResponse)
async def update_my_profile(admin_update: AdminUpdate, current_admin: AdminResponse = Depends(get_current_user)):
    try:
        return await admin_service.update_admin(admin_update, current_admin)
    except UnauthorizedException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except AdminAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PasswordMismatchException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AdminNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
#------------------------Logout admin---------------------  
@router.post("/logout-admin")
async def logout_admin(
    token: str = Depends(oauth2_scheme), 
    current_admin=Depends(get_current_admin)
):
    try:
        return await admin_service.logout_admin(token, current_admin)
    except UnauthorizedException as e:
        raise HTTPException(status_code=403, detail=str(e))
    
# ----------------- Delete Admin Endpoint -----------------
@router.delete("/delete-admin", response_model=dict)
async def delete_my_admin(current_admin: dict = Depends(get_current_admin)):
    try:
        return await admin_service.delete_admin(current_admin)
    except AdminNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))