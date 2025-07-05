from db import expenses,save_to_file
from models import Expense,UpdateExpense
from logger import logger

async def create_expense(expense: Expense):
    if expense.id in expenses:
        logger.warning(f"Create failed: Expense ID {expense.id} already exists")
        return False
    expenses[expense.id] = expense.model_dump()
    save_to_file()
    logger.info(f"Created new expense: {expense.id}")
    return True

async def get_expense(expense_id:str):
    if expense_id not in expenses:
        logger.error(f"Get failed: Expense ID {expense_id} not found")
        return None
    logger.info(f"Fetched expense: {expense_id}")
    return expenses.get(expense_id) 

async def get_all_expenses():
    logger.info("Fetched all expenses")
    return list(expenses.values())


async def update_expense(expense_id: str, data: UpdateExpense):
    if expense_id not in expenses:
        logger.error(f"Update failed: Expense ID '{expense_id}' not found")
        return None
    current = expenses[expense_id]
    updated = current.copy()
    if data.title is not None:
        updated['title'] = data.title
    if data.amount is not None:
        updated['amount'] = data.amount
    if data.category is not None:
        updated['category'] = data.category
    #updated = current.copy(update=data.(exclude_unset=True))
    expenses[expense_id] = updated
    logger.info(f"Updated expense: {expense_id}")
    return updated

async def delete_expense(expense_id: str):
    if expense_id not in expenses:
        logger.error(f"Delete failed: Expense ID '{expense_id}' not found")
        return False
    del expenses[expense_id]
    save_to_file()
    logger.info(f"Deleted expense: {expense_id}")
    return True