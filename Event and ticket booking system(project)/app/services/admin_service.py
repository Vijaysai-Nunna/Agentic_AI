from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.context import CryptContext

from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

from bson import ObjectId
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from database.connection import db
from database.collections import users_collection

from app.models.admin_model import AdminCreate, AdminLogin, AdminResponse,AdminUpdate

from app.auth.auth_service import get_current_user
from app.auth.auth_service import get_current_admin

from app.utils.token_utils import blacklist_token
from app.utils.sequence_utils import get_next_admin_id
from app.utils.logging_utils import get_logger
from app.utils.exceptions import (
    UserAlreadyExistsException,
    PasswordMismatchException,
    InvalidCredentialsException,
    UnauthorizedException,
    AdminNotFoundException,
    AdminAlreadyExistsException
)


logger = get_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Password utils
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT utils
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Admin Service
class AdminService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["admins"]

#-----------------Register admin--------------------
    async def register_admin(self, admin: AdminCreate, current_user: Optional[AdminResponse] = Depends(get_current_user)) -> AdminResponse:
    # Only first admin can self-register
        count = await self.collection.count_documents({})
        if count > 0:
            if not current_user or current_user.role != "admin":
                raise UnauthorizedException("Only admins can register new admins")

    # Password check
        if admin.password != admin.confirm_password:
            raise PasswordMismatchException("Password and Confirm Password do not match")

    # Check email uniqueness
        if await self.collection.find_one({"email": admin.email}):
            raise AdminAlreadyExistsException("Email already exists")

    # Check full_name uniqueness
        if await self.collection.find_one({"Full_name": admin.Full_name}):
            raise AdminAlreadyExistsException("Admin Full name already exists")

    # Check reused password
        async for existing_admin in self.collection.find({}, {"password": 1}):
            if existing_admin.get("password") and verify_password(admin.password, existing_admin["password"]):
                raise AdminAlreadyExistsException("This password is already in use, choose another one")

    # Hash password
        hashed_password = get_password_hash(admin.password)

    # Sequence ID
        admin_id = await get_next_admin_id()

        admin_doc = {
            "admin_id": admin_id,
            "Full_name": admin.Full_name,
            "email": admin.email,
            "phone": admin.phone,
            "password": hashed_password,
            "is_active": True,
            "role": "admin",
            "created_at": datetime.utcnow(),
    }

        result = await self.collection.insert_one(admin_doc)
        logger.info(f"Admin registered: {admin.email} | admin_id={admin_id}")

    # Return AdminResponse instead of dict
        return AdminResponse(
            id=str(result.inserted_id),
            admin_id=admin_doc["admin_id"],
            Full_name=admin_doc["Full_name"],
            email=admin_doc["email"],
            phone=admin_doc["phone"],
            is_active=admin_doc["is_active"],
            role=admin_doc["role"],
            created_at=admin_doc["created_at"]
    )
    
#-------------Login Admin-------------------
    async def login_admin(self, login: AdminLogin) -> dict:
        admin = await self.collection.find_one({"email": login.email})
        if not admin:
            raise AdminNotFoundException("Admin not found")

        if not verify_password(login.password, admin["password"]):
            raise InvalidCredentialsException("Invalid email or password")

    # Token payload
        token_data = {"sub": admin["email"], "id": str(admin["_id"]), "role": "admin"}
        access_token = create_access_token(token_data)

    # Build response
        return {
            "message": f"Admin {admin['Full_name']} logged in successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "admin": AdminResponse(
                id=str(admin["_id"]),
                admin_id=admin["admin_id"],
                Full_name=admin["Full_name"],
                email=admin["email"],
                phone=admin["phone"],
                is_active=admin["is_active"],
                role=admin["role"],
                created_at=admin["created_at"]
        )
    }
    
#-------------------Get _current admin info-------------------
    async def get_current_admin(self, current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.role != "admin":
            raise UnauthorizedException("Only admins can access this endpoint")

        admin = await self.collection.find_one({"_id": ObjectId(current_user.id)})
        if not admin:
            raise AdminNotFoundException("Admin not found")

        return {
            "id": str(admin["_id"]),
            "admin_id": admin["admin_id"],
            "Full_name": admin["Full_name"],
            "email": admin["email"],
            "phone": admin["phone"],
            "is_active": admin["is_active"],
            "role": admin["role"],
            "created_at": admin["created_at"],
        }

# ---------------- Get All Users ----------------
    async def get_all_users(self, current_user: dict = Depends(get_current_user)) -> list:
        if current_user.role != "admin":
            raise UnauthorizedException("Only admins can view all users")

        users = []
        async for user in users_collection.find({}):
            users.append({
                "id": str(user["_id"]),
                "user_id": user["user_id"],
                "Full_name": user["Full_name"],
                "email": user["email"],
                "phone": user["phone"],
                "is_active": user["is_active"],
                "role": user.get("role", "user"),
                "created_at": user["created_at"],
            })

        return users
    

# ----------------- Get All Admins --------------------
    async def get_all_admins(self, current_admin: AdminResponse) -> list:
    # Ensure only admins can access
        if current_admin.role != "admin":
            raise UnauthorizedException("Only admins can access this resource")

        admins = []
        async for admin in self.collection.find({}):
            admins.append(AdminResponse(
                id=str(admin["_id"]),
                admin_id=admin["admin_id"],
                Full_name=admin["Full_name"],
                email=admin["email"],
                phone=admin["phone"],
                is_active=admin["is_active"],
                role=admin["role"],
                created_at=admin["created_at"]
        ))
        return admins
    

# ----------------- Update Admin Profile --------------------
    async def update_admin(self, admin_update: AdminUpdate, current_admin: AdminResponse) -> AdminResponse:
        if current_admin.role != "admin":
            raise UnauthorizedException("Only admins can update their profile")

        admin_doc = await self.collection.find_one({"_id": ObjectId(current_admin.id)})
        if not admin_doc:
            raise AdminNotFoundException("Admin not found")

        update_data = {}

    # Check Full_name uniqueness
        if admin_update.Full_name and admin_update.Full_name != admin_doc["Full_name"]:
            if await self.collection.find_one({"Full_name": admin_update.Full_name}):
                raise AdminAlreadyExistsException("Full_name already in use")
            update_data["Full_name"] = admin_update.Full_name

    # Check email uniqueness
        if admin_update.email and admin_update.email != admin_doc["email"]:
            if await self.collection.find_one({"email": admin_update.email}):
                raise AdminAlreadyExistsException("Email already in use")
            update_data["email"] = admin_update.email

    # Check phone uniqueness
        if admin_update.phone and admin_update.phone != admin_doc["phone"]:
            if await self.collection.find_one({"phone": admin_update.phone}):
                raise AdminAlreadyExistsException("Phone already in use")
            update_data["phone"] = admin_update.phone

    # Password update
        if admin_update.old_password or admin_update.new_password or admin_update.confirm_password:
            if not admin_update.old_password or not admin_update.new_password or not admin_update.confirm_password:
                raise PasswordMismatchException("Provide old_password, new_password, and confirm_password to change password")
            if not verify_password(admin_update.old_password, admin_doc["password"]):
                raise PasswordMismatchException("Old password is incorrect")
            if admin_update.old_password == admin_update.new_password:
                raise PasswordMismatchException("New password cannot be the same as old password")
            if admin_update.new_password != admin_update.confirm_password:
                raise PasswordMismatchException("New password and confirm password do not match")
            update_data["password"] = get_password_hash(admin_update.new_password)

        if not update_data:
            raise PasswordMismatchException("No new data provided for update")

        update_data["updated_at"] = datetime.utcnow()

        await self.collection.update_one({"_id": ObjectId(current_admin.id)}, {"$set": update_data})

    # Return updated AdminResponse
        admin_doc.update(update_data)
        return AdminResponse(
            id=str(admin_doc["_id"]),
            admin_id=admin_doc["admin_id"],
            Full_name=admin_doc["Full_name"],
            email=admin_doc["email"],
            phone=admin_doc["phone"],
            is_active=admin_doc["is_active"],
            role=admin_doc["role"],
            created_at=admin_doc["created_at"]
    )


#-------------------------logout admin-------------------
    async def logout_admin(self, token: str, current_admin: AdminResponse) -> dict:
        """
        Logout admin by blacklisting their JWT token
        """
        if current_admin.role != "admin":
            raise UnauthorizedException("Only admins can logout")

        # Blacklist the token
        blacklist_token(token)

        return {"message": f"Admin {current_admin.Full_name} logged out successfully"}

#-----------------------Delete Admin----------------
    async def delete_admin(self, current_admin: AdminResponse = Depends(get_current_admin)) -> dict:
        """
        Delete the current admin account
        """
        admin = await self.collection.find_one({"_id": ObjectId(current_admin.id)})
        if not admin:
            raise AdminNotFoundException("Admin not found")

        result = await self.collection.delete_one({"_id": ObjectId(current_admin.id)})
        if result.deleted_count == 1:
            return {"message": f"Admin {current_admin.Full_name} deleted successfully"}
        else:
            raise AdminNotFoundException("Admin deletion failed")