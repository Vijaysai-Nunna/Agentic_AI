from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends

from database.collections import users_collection
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from app.models.user_model import UserResponse
from app.utils.logging_utils import get_logger
from app.utils.exceptions import InvalidCredentialsException

from bson import ObjectId

# Setup 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = get_logger(__name__)

# OAuth2 scheme (token URL points to login endpoint in auth_router)
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Password Utils 
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


#  JWT Token Utils 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"JWT token created for user: {data.get('sub')}")
    return encoded_jwt


# Authenticate User 
async def authenticate_user(email: str, password: str) -> Optional[dict]:
    user = await users_collection.find_one({"email": email})
    if not user:
        logger.warning(f"Authentication failed: user not found ({email})")
        return None
    if not verify_password(password, user["password"]):
        logger.warning(f"Authentication failed: wrong password for ({email})")
        return None

    logger.info(f"Authentication successful: {email}")
    return user


# Get Current User (from token) 
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: str = payload.get("id")

        if email is None or user_id is None:
            logger.error("JWT payload invalid: missing email or user_id")
            raise InvalidCredentialsException()
    except JWTError as e:
        logger.error(f"JWT decoding failed: {str(e)}")
        raise InvalidCredentialsException()

    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        logger.error(f"JWT token valid but user not found in DB (ID: {user_id})")
        raise InvalidCredentialsException()

    logger.info(f"JWT token validated successfully for user: {email}")
    return UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        phone=user["phone"],
        is_active=user["is_active"],
        is_admin=user["is_admin"],
    )
