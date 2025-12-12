from fastapi import FastAPI
from routers import expenses
from logger import logger



app = FastAPI()
app.include_router(expenses.router)
logger.info("Expense Tracker API started")  