from fastapi import APIRouter, Depends, HTTPException
from database.connection import db
from app.models.user_model import UserCreate, UserLogin, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.utils.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
)

router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService(db)

# Register user
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    try:
        return await user_service.register_user(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))

# Login user
@router.post("/login")
async def login_user(login: UserLogin):
    try:
        response = await user_service.login_user(login)
        return {"message":f"User Logged in Successfully :{login.email}",**response}
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=str(e))


# # Update user
# @router.put("/update/{user_id}", response_model=UserResponse)
# async def update_user(user_id: str, update_data: UserUpdate):
#     try:
#         return await user_service.update_user(user_id, update_data)
#     except UserAlreadyExistsException as e:  # duplicate password case
#         raise HTTPException(status_code=400, detail=str(e))
#     except UserNotFoundException as e:
#         raise HTTPException(status_code=404, detail=str(e))

# # Delete user
# @router.delete("/delete/{user_id}")
# async def delete_user(user_id: str):
#     try:
#         return await user_service.delete_user(user_id)
#     except UserNotFoundException as e:
#         raise HTTPException(status_code=404, detail=str(e))
