from pydantic import BaseModel
from typing import Optional

class Expense(BaseModel):
    id:str
    title:str
    amount:float
    category:str

class UpdateExpense(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None

class DeleteExpense(BaseModel):
    id:str