from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId

from database.connection import db
from app.models.user_model import UserCreate, UserLogin, UserUpdate
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.logging_utils import get_logger
from app.utils.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
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

# Sequence Generator
async def get_next_user_id():
    counters = db["counters"]
    result = await counters.find_one_and_update(
        {"_id": "user_id"},
        {"$inc": {"sequence_value": 1}},
        return_document=True,
        upsert=True
    )
    return f"USR{result['sequence_value']:03d}" 

# User Service 
class UserService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    # Register user
    async def register_user(self, user: UserCreate) -> dict:
        # Check if email already exists
        existing = await self.collection.find_one({"email": user.email})
        if existing:
            logger.warning(f"Registration failed: User with email {user.email} already exists")
            raise UserAlreadyExistsException("Email already exists")

        # Check if password already exists
        async for existing_user in self.collection.find({}, {"password": 1}):
            stored_hash = existing_user.get("password")
            if stored_hash and verify_password(user.password, stored_hash):
                logger.warning("Registration failed: Password already used by another user")
                raise UserAlreadyExistsException("This password is already in use, choose another one.")
# Hash the new password
        hashed_password = get_password_hash(user.password)
# Generate custom user_id
        user_id = await get_next_user_id()
        user_doc = {
            "user_id": user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "password": hashed_password,
            "is_active": True,
            "is_admin": False,
            "created_at": datetime.utcnow()
        }

        result = await self.collection.insert_one(user_doc)
        logger.info(f"User registered: {user.email} | user_id={user_id} | _id={result.inserted_id}")

        return {**user_doc, "id": str(result.inserted_id)}

# Login user
    async def login_user(self, login: UserLogin) -> dict:
        user = await self.collection.find_one({"email": login.email})
        if not user or not verify_password(login.password, user["password"]):
            logger.warning(f"Login failed for email: {login.email}")
            raise InvalidCredentialsException("Invalid email or password")

        token_data = {"sub": user["email"], "id": str(user["_id"])}
        access_token = create_access_token(token_data)
        logger.info(f"User logged in successfully: {login.email}")
        return {"message":f"User Logged in Successfully :{login.email}","access_token": access_token, "token_type": "bearer"}


    # # Update user (by _id or user_id)
    # async def update_user(self, user_id: str, update_data: UserUpdate) -> dict:
    #     update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    #     if "password" in update_dict:
    #         # prevent duplicate password reuse
    #         async for existing_user in self.collection.find({}, {"password": 1}):
    #             if verify_password(update_dict["password"], existing_user["password"]):
    #                 logger.warning("Update failed: Password already used by another user")
    #                 raise UserAlreadyExistsException("This password is already in use, choose another one.")
    #         update_dict["password"] = get_password_hash(update_dict["password"])

    #     query = {"_id": ObjectId(user_id)} if ObjectId.is_valid(user_id) else {"user_id": user_id}
    #     result = await self.collection.update_one(query, {"$set": update_dict})
    #     if result.matched_count == 0:
    #         logger.error(f"User update failed: {user_id} not found")
    #         raise UserNotFoundException("User not found")

    #     return await self.get_user_by_id(user_id)

    # # Delete user (by _id or user_id)
    # async def delete_user(self, user_id: str) -> dict:
    #     query = {"_id": ObjectId(user_id)} if ObjectId.is_valid(user_id) else {"user_id": user_id}
    #     result = await self.collection.delete_one(query)
    #     if result.deleted_count == 0:
    #         logger.error(f"User deletion failed: {user_id} not found")
    #         raise UserNotFoundException("User not found")

    #     logger.info(f"User deleted successfully: {user_id}")
    #     return {"message": f"User {user_id} deleted successfully"}
