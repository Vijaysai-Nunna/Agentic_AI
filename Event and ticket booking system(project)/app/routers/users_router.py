from fastapi import APIRouter, Depends, HTTPException, status

from database.connection import db

from app.models.user_model import UserCreate, UserLogin, UserUpdate, UserResponse

from app.services.user_service import UserService

from app.auth.auth_service import get_current_user,oauth2_scheme

from app.utils.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    PasswordMismatchException,
)

router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService(db)


#-------------Register User-----------------
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    try:
        return await user_service.register_user(user)
    except (UserAlreadyExistsException, PasswordMismatchException) as e:
        raise HTTPException(status_code=400, detail=str(e))


#----------------------Login User------------------------
@router.post("/login")
async def login_user(login: UserLogin):
    try:
        return await user_service.login_user(login)
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=str(e))


#----------------------User Info --------------------------------
@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: UserResponse = Depends(get_current_user)):
    return await user_service.get_my_profile(current_user)

#-------------------------update user----------------------
@router.put("/update", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate, current_user: UserResponse = Depends(get_current_user)
):
    try:
        return await user_service.update_user(current_user, update_data)
    except (UserAlreadyExistsException, InvalidCredentialsException, PasswordMismatchException) as e:
        raise HTTPException(status_code=400, detail=str(e))

#-----------------------------Logout User---------------------------    
@router.post("/logout")
async def logout(current_user=Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    try:
        return await user_service.logout_user(token, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

#----------------------------------Delete User---------------------------
@router.delete("/delete", response_model=dict)
async def delete_profile(current_user=Depends(get_current_user)):
    try:
        return await user_service.delete_user(current_user)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))