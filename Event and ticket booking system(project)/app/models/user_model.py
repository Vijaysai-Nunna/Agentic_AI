from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


#-------------------User Base----------------
class UserBase(BaseModel):
    Full_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=10)

#----------------User Create------------------------
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)
    role: Optional[str] = Field(default="user")

#--------------------User Login-------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#------------------User Response--------------
class UserResponse(UserBase):
    id: str           
    user_id: str  
    Full_name:str  
    is_active: bool
    role:str = "user"
    created_at: datetime

    class Config:
        from_attributes = True

#----------------------User Update------------------------
class UserUpdate(BaseModel):
    Full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None
    confirm_password: Optional[str] = None
    role: Optional[str] = None 


    class Config:
        from_attributes = True
