from pydantic import BaseModel 
from typing import Optional

class Employee(BaseModel):
    emp_id:str
    name:str 
    position:str
    salary:float 
    area:str

class EmployeeUpdate(BaseModel):
    emp_id: Optional[str] = None
    name: Optional[str] = None 
    position: Optional[str] = None 
    salary: Optional[float] = None 
    area: Optional[str] = None