import time
from typing import Dict
from fastapi import HTTPException
from bson import ObjectId
from app.utils.email_service import send_reset_email
from app.utils.logger import setup_logger
from app.db.mongo import collection
from app.models.user_model import UserProfile, ChangePasswordRequest
from app.utils.auth import hash_password, verify_password, create_access_token, password_is_valid, generate_reset_token
from datetime import datetime, timedelta
logger = setup_logger()

password_history = {}
reset_requests = {}

async def register_user(user):
    if not password_is_valid(user.password):
        logger.error(f"Password vlidation failed for username:{user.username}")
        raise ValueError("Password does not meet complexity requirements")
    
    hashed_password = hash_password(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "confirm_password": hashed_password,
        "phone": user.phone,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "dob": user.dob,
        "doj": user.doj,
        "address": user.address,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    existing_user = collection.find_one({"$or": [{"username":user.username},{"email": user.email}]})
    if existing_user:
        logger.warning(f"User with Username {user.username} email {user.email} already exists.")
        raise ValueError("Username or email already exists.")
    
    result = collection.insert_one(user_data)
    logger.info(f"User {user.username} registered successfully at {datetime.now()}")
    password_history[user.username] = [hashed_password]
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}


async def login_user(username, password):
    user = collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        logger.error(f"Login failed for username: {username}")
        raise ValueError("Invalid username or password")
    
    access_token = create_access_token({"sub": username})
    logger.info(f"User {username} logged in successfully at {datetime.now()}")
    return {"message":"login succesful", "access_token": access_token, "token_type": "bearer"} 


async def update_user_profile(current_user: Dict, updates: UserProfile):
    username = current_user.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="Missing username in token payload")
    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    if not update_data:
        raise ValueError("No valid fields to update")
    result = collection.update_one(
        {"username": username},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        logger.warning(f"No update made for user {username}")
        raise ValueError("Update failed or no changes detected")
    logger.info(f"User profile updated for {username}")
    return {"message": "Profile updated successfully"}



async def change_user_password(current_user: dict, data: ChangePasswordRequest):
    username = current_user.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="Missing username in token")
    user = collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.old_password, user["password"]):
        raise HTTPException(status_code=403, detail="Old password is incorrect")
    if not password_is_valid(data.new_password):
        raise HTTPException(status_code=400, detail="New password does not meet complexity requirements")

    hashed_password = hash_password(data.new_password)
    result = collection.update_one(
        {"username": username},
        {"$set": {"password": hashed_password}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Password update failed")
    logger.info(f"Password updated for user {username}")
    return {"message": "Password changed successfully"}


async def forget_password(username, email):
    print("[DEBUG] forget_password called")
    user = collection.find_one({"username": username, "email": email})
    if not user:
        print("[DEBUG] No user found with given username and email")
        raise HTTPException(status_code=404, detail="Invalid username or email")

    reset_token = generate_reset_token(username)
    reset_requests[username] = reset_token
    print(f"[DEBUG] Generated reset token: {reset_token}")

    send_reset_email(email, reset_token)
    return {"message": "Reset token sent to your email"}


async def reset_password(username: str, reset_token: str, new_password: str):
    expected_token = reset_requests.get(username)
    if not expected_token or expected_token != reset_token:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    if not password_is_valid(new_password):
        raise HTTPException(status_code=400, detail="Password does not meet complexity requirements")

    hashed_password = hash_password(new_password)
    result = collection.update_one(
        {"username": username},
        {"$set": {"password": hashed_password}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Password reset failed")

    logger.info(f"Password reset successful for user {username}")
    del reset_requests[username]
    return {"message": "Password has been reset successfully"}


async def logout_user(current_user: dict):
    username = current_user.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="Missing username in token")

    logger.info(f"User {username} logged out at {datetime.now()}")
    return {"message": f"User {username} logged out successfully"}