from fastapi import APIRouter, HTTPException
from models import Expense, UpdateExpense
from models import UpdateExpense
from crud import (
    create_expense, get_expense, get_all_expenses,
    update_expense,delete_expense
)

router = APIRouter()

@router.post("/create-expense")
async def add_expense(expense: Expense):
    if not await create_expense(expense):
        raise HTTPException(status_code=400, detail="Expense ID already exists")
    return {"message": "Expense added"}

@router.get("/list-expenses")
async def list_expenses():
    return await get_all_expenses()

@router.get("/get-expense/{expense_id}")
async def get_expense_by_id(expense_id: str):
    expense = await get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.put("/update-expense/{expense_id}")
async def update_expense_by_id(expense_id: str, data: UpdateExpense):
    updated_expense = await update_expense(expense_id, data)
    if not updated_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense updated", "expense": updated_expense}


@router.delete("/delete-expense/{expense_id}")
async def delete_expense_by_id(expense_id: str):
    if not await delete_expense(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted"}