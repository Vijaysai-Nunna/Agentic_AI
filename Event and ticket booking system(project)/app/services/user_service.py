from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.context import CryptContext

from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

from bson import ObjectId

from database.connection import db

from app.auth.auth_service import get_current_user

from app.models.user_model import UserCreate, UserLogin, UserUpdate, UserResponse

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from app.utils.sequence_utils import get_next_user_id
from app.utils.token_utils import blacklist_token
from app.utils.logging_utils import get_logger
from app.utils.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    PasswordMismatchException,
)

logger = get_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Password Utils
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT Token Utils 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# User Service 
class UserService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

#---------------------Register user------------------
    async def register_user(self, user: UserCreate) -> UserResponse:
        if user.password != user.confirm_password:
            logger.warning("Passwords do not match")
            raise PasswordMismatchException("Password and Confirm Password do not match")

        # Check unique email and username
        if await self.collection.find_one({"email": user.email}):
            raise UserAlreadyExistsException("Email already exists")
        if await self.collection.find_one({"name": user.Full_name}):
            raise UserAlreadyExistsException("Username already exists")

        # Check password reuse (optional, expensive for large DB)
        async for existing_user in self.collection.find({}, {"password": 1}):
            if verify_password(user.password, existing_user.get("password", "")):
                raise UserAlreadyExistsException("This password is already used by another user")

        hashed_password = get_password_hash(user.password)
        user_id = await get_next_user_id()
        role = user.role if user.role else "user"

        user_doc = {
            "user_id": user_id,
            "Full_name": user.Full_name,
            "email": user.email,
            "phone": user.phone,
            "password": hashed_password,
            "is_active": True,
            "role": role,
            "created_at": datetime.utcnow()
        }

        result = await self.collection.insert_one(user_doc)
        logger.info(f"User registered: {user.email} | user_id={user_id}")

        return UserResponse(
            id=str(result.inserted_id),
            user_id=user_id,
            Full_name=user.Full_name,
            email=user.email,
            phone=user.phone,
            is_active=True,
            role=role,
            created_at=user_doc["created_at"]
        )

# ---------------------------------Login user--------------------
    async def login_user(self, login: UserLogin) -> dict:
        user = await self.collection.find_one({"email": login.email})
        if not user or not verify_password(login.password, user["password"]):
            raise InvalidCredentialsException("Invalid email or password")

        if not user.get("is_active", True):
            raise InvalidCredentialsException("Account inactive. Contact admin.")

        token_data = {"sub": user["email"], "id": str(user["_id"]), "role": user["role"]}
        access_token = create_access_token(token_data)

        logger.info(f"User logged in: {login.email}")
        return {
            "message": f"User logged in successfully: {user['Full_name']}",
            "access_token": access_token,
            "token_type": "bearer",
            "user":UserResponse(
                id=str(user["_id"]),
                user_id=user["user_id"],
                Full_name=user["Full_name"],
                email=user["email"],
                phone=user["phone"],
                is_active=user["is_active"],
                role=user["role"],
                created_at=user["created_at"]

            )
        }

#----------------------------- Get own profile----------------------
    async def get_my_profile(self, current_user: UserResponse) -> UserResponse:
        user = await self.collection.find_one({"_id": ObjectId(current_user.id)})
        if not user:
            raise UserNotFoundException("User not found")

        return UserResponse(
            id=str(user["_id"]),
            user_id=user["user_id"],
            Full_name=user["Full_name"],
            email=user["email"],
            phone=user["phone"],
            is_active=user["is_active"],
            role=user.get("role", "user"),
            created_at=user["created_at"]
        )
    


 #---------------------------------Update User-------------------------- 
    async def update_user(
        self, current_user: UserResponse, update_data: UserUpdate
    ) -> dict:
        """Update user profile with validations"""

        # Fetch existing user from DB
        user = await self.collection.find_one({"_id": ObjectId(current_user.id)})
        if not user:
            raise UserNotFoundException("User not found")

        # No update provided
        if not any([
            update_data.Full_name, update_data.email, update_data.phone,
            update_data.old_password, update_data.new_password, update_data.confirm_password
        ]):
            raise InvalidCredentialsException("No new data provided for update")

        update_fields = {}

        # Name/email/phone updates
        if update_data.Full_name and update_data.Full_name != user["name"]:
            # Check name uniqueness
            existing_name = await self.collection.find_one({"name": update_data.Full_name})
            if existing_name:
                raise UserAlreadyExistsException("Username already exists")
            update_fields["name"] = update_data.Full_name

        if update_data.email and update_data.email != user["email"]:
            # Check email uniqueness
            existing_email = await self.collection.find_one({"email": update_data.email})
            if existing_email:
                raise UserAlreadyExistsException("Email already exists")
            update_fields["email"] = update_data.email

        if update_data.phone and update_data.phone != user["phone"]:
            update_fields["phone"] = update_data.phone

        # Password update logic
        if update_data.old_password or update_data.new_password or update_data.confirm_password:
            if not all([update_data.old_password, update_data.new_password, update_data.confirm_password]):
                raise InvalidCredentialsException(
                    "Old password, new password, and confirm password are required for password update"
                )
            # Verify old password
            if not verify_password(update_data.old_password, user["password"]):
                raise InvalidCredentialsException("Old password is incorrect")
            # Old and new should not match
            if update_data.old_password == update_data.new_password:
                raise PasswordMismatchException("New password cannot be same as old password")
            # New and confirm should match
            if update_data.new_password != update_data.confirm_password:
                raise PasswordMismatchException("New password and confirm password do not match")
            # Hash new password
            update_fields["password"] = get_password_hash(update_data.new_password)

        if update_fields:
            await self.collection.update_one({"_id": ObjectId(current_user.id)}, {"$set": update_fields})
            # Return updated user
            user.update(update_fields)

        return {
            "id": str(user["_id"]),
            "user_id": user["user_id"],
            "Full_name": user["Full_name"],
            "email": user["email"],
            "phone": user["phone"],
            "role": user.get("role", "user"),
            "is_active": user["is_active"],
            "created_at": user["created_at"]
        }


#----------------------------------Logout User--------------------------
    async def logout_user(self, token: str, current_user: UserResponse) -> dict:
        """
        Logout the current user by blacklisting the token
        """
        blacklist_token(token)
        return {"message": f"User {current_user.Full_name} logged out successfully"}
    

#------------------------------------------Delete user--------------------------------
    async def delete_user(self, current_user: UserResponse) -> dict:
        """Delete user profile using login token"""
        result = await self.collection.delete_one({"_id": ObjectId(current_user.id)})
        if result.deleted_count == 0:
            raise UserNotFoundException("User not found or already deleted")

        return {"message": f"User {current_user.Full_name} deleted successfully"}