from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.auth.auth_service import create_access_token, verify_token
from app.auth.auth_service import authenticate_user, create_access_token

from config import ACCESS_TOKEN_EXPIRE_MINUTES

from app.utils.logging_utils import get_logger
from app.utils.exceptions import InvalidCredentialsException

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ----------------Login Endpoint----------------------
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.warning(f"OAuth2 login failed for username/email: {form_data.username}")
        raise InvalidCredentialsException()

    token_data = {"sub": user["email"], "id": str(user["_id"])}
    access_token = create_access_token(token_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    logger.info(f"OAuth2 login successful for user: {user['email']}")
    return {"access_token": access_token, "token_type": "bearer"}

#----------------------------Verify Endpoint--------------------
@router.get("/verify")
async def verify(current_user: dict = Depends(verify_token)):
    """
    Verify token endpoint: returns decoded user info
    """
    return {"status": "success", "user": current_user}
