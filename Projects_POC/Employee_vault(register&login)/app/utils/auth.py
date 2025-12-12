from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi import HTTPException,status, Depends,Header
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
  return pwd_context.hash(password)

def verify_password(plain, hashed):
  return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def password_is_valid(password):
   return (
     8 <= len(password) <= 20
     and any(c.islower() for c in password)
     and any(c.isupper() for c in password)
     and any(c.isdigit() for c in password)
     and any(c in '!@#$%^&*()-_+=' for c in password)
     )

def generate_reset_token(username):
   expire = datetime.utcnow() + timedelta(hours=24)
   return f"{username}:{expire.timestamp()}"



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(authorization: str = Header(...)):
    try:
        if not authorization.startswith("Bearer"):
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        token = authorization.replace("Bearer", "").strip()
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # FIX HERE: use 'sub' because that's how it's stored
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        return {"username": username}  # return a consistent user dict
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")
 
