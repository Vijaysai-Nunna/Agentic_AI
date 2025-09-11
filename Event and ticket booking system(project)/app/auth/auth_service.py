from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from database.collections import users_collection,admins_collection
from database.connection import db

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from app.models.admin_model import AdminResponse
from app.models.user_model import UserResponse

from app.utils.logging_utils import get_logger
from app.utils.exceptions import InvalidCredentialsException,UnauthorizedException
from app.utils.token_utils import is_token_blacklisted
from database.connection import db

admins_collection = db["admins"]
users_collection = db["users"]


# Logger setup
logger = get_logger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Password Utils
# ----------------------
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT Token Utils
# ----------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generate a JWT token with expiration"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"JWT token created for user: {data.get('sub')}")
    return token


# Authenticate User
# ----------------------
async def authenticate_user(email: str, password: str) -> Optional[dict]:
    user = await users_collection.find_one({"email": email})
    if not user:
        logger.warning(f"Authentication failed: user not found ({email})")
        return None
    if not verify_password(password, user["password"]):
        logger.warning(f"Authentication failed: wrong password ({email})")
        return None

    logger.info(f"Authentication successful: {email}")
    return user


# Get Current User (User or Admin)
# ----------------------
async def get_current_user(token: str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise InvalidCredentialsException("Token is invalid or user logged out")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        email: str = payload.get("sub")
        role: str = payload.get("role", "user")
        if not user_id or not email:
            raise InvalidCredentialsException("Invalid token payload")
    except JWTError as e:
        logger.error(f"JWT decoding failed: {str(e)}")
        raise InvalidCredentialsException()

    if role == "admin":
        admin = await admins_collection.find_one({"_id": ObjectId(user_id)})
        if not admin:
            raise InvalidCredentialsException("Admin not found")

        return AdminResponse(
            id=str(admin["_id"]),
            admin_id=admin["admin_id"],
            Full_name=admin["Full_name"],
            email=admin["email"],
            phone=admin["phone"],
            is_active=admin["is_active"],
            role="admin",
            created_at=admin["created_at"]
        )

    # Default to user
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise InvalidCredentialsException("User not found")

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

def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise InvalidCredentialsException()
    

# ----------------- Get current admin -----------------
async def get_current_admin(token: str = Depends(oauth2_scheme)) -> AdminResponse:
    """
    Get the current logged-in admin from token
    """
    if is_token_blacklisted(token):
        raise InvalidCredentialsException("Token is invalid or admin logged out")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded payload in get_current_admin: {payload}")
        admin_id: str = payload.get("id")
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if not admin_id or not email:
            raise InvalidCredentialsException("Invalid token payload")
        if role != "admin":
            raise UnauthorizedException("Only admins can access this resource")
    except JWTError as e:
        logger.error(f"JWT decoding failed in get_current_admin: {str(e)}")
        raise InvalidCredentialsException("Invalid token")
    
    admin = await db["admins"].find_one({"_id": ObjectId(admin_id)})
    if not admin:
        raise InvalidCredentialsException("Admin not found")

    return AdminResponse(
        id=str(admin["_id"]),
        admin_id=admin["admin_id"],
        Full_name=admin["Full_name"],
        email=admin["email"],
        phone=admin["phone"],
        is_active=admin["is_active"],
        role=admin.get("role", "admin"),
        created_at=admin["created_at"]
    )