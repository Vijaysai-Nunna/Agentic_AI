from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


#---------------AdminBase-----------------
class AdminBase(BaseModel):
    Full_name: str
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=10)

#-----------------Admin Create---------------
class AdminCreate(AdminBase):
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)


#-----------------Admin Login--------------
class AdminLogin(BaseModel):
    email: EmailStr
    password: str

#------------------Admin Response--------------
class AdminResponse(AdminBase):
    id: str
    admin_id: str
    Full_name:str
    is_active: bool
    role: str = "admin"
    created_at: datetime

#-----------------Admin Update------------------
class AdminUpdate(BaseModel):
    Full_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=10)
    old_password: Optional[str] = Field(None, min_length=6)
    new_password: Optional[str] = Field(None, min_length=6)
    confirm_password: Optional[str] = Field(None, min_length=6)

    class Config:
        from_attributes = True
