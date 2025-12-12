from fastapi import APIRouter, Depends, Request, HTTPException
from app.models.user_model import RegisterUser, UserProfile, ForgetPasswordRequest,ChangePasswordRequest, ResetPasswordRequest, logoutRequest
from app.services.user_service import register_user,login_user,update_user_profile,change_user_password,forget_password,reset_password,logout_user
from app.utils.decorators import handle_exceptions
from app.utils.auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register")
@handle_exceptions
async def register(user: RegisterUser):
    if not user.username or not user.password or not user.confirm_password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    return await register_user(user)

@router.post("/login")
@handle_exceptions
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    return await login_user(username, password)

# @router.put("/update_profile")
# @handle_exceptions
# async def update_profile(updates:UserProfile, current_user:dict =Depends(get_current_user)):
#      try:
#           return await update_profile(current_user['username'], updates)
#      except ValueError as e:
#          raise HTTPException(status_code=400, detail=str(e))
#      except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal Server Error")



@router.put("/update_profile")
@handle_exceptions
async def update_profile(
    updates: UserProfile,
    current_user: dict = Depends(get_current_user)
):
    try:
        return await update_user_profile(current_user, updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("Internal Server Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.put("/change_password")
@handle_exceptions
async def change_password(
    data: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user)
):
    return await change_user_password(current_user, data)


@router.post("/forget_password")
@handle_exceptions
async def forgot_password(request: ForgetPasswordRequest):
    return await forget_password(request.username, request.email)

@router.post("/reset_password")
@handle_exceptions
async def reset_user_password(request: ResetPasswordRequest):
    return await reset_password(request.username, request.reset_token, request.new_password)


@router.post("/logout")
@handle_exceptions
async def logout(current_user: dict = Depends(get_current_user)):
    return await logout_user(current_user)
  
    