from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str           
    user_id: str    
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr] 
    phone: Optional[str]
    password: Optional[str]

    class Config:
        from_attributes = True
