from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class RegisterUser(BaseModel):
  username: str
  email: str
  phone: str
  first_name: str
  last_name: str
  dob: str
  doj: str
  address: str
  password: str
  confirm_password: str

class LoginUser(BaseModel):
  username: str
  password: str

class UserProfile(BaseModel):
  username: Optional[str]= None
  email: Optional[EmailStr] = None  
  phone: Optional[str] = None
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  dob: Optional[date] = None
  doj: Optional[date] = None
  address: Optional[str] = None

class ChangePasswordRequest(BaseModel):
  old_password: str
  new_password: str

class ForgetPasswordRequest(BaseModel):
    username: str
    email: str

class ResetPasswordRequest(BaseModel):
    username: str
    reset_token: str
    new_password: str

class logoutRequest(BaseModel):
  username: str