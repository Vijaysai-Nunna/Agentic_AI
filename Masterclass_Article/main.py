from fastapi import FastAPI 
from app.routers import employee_router

app = FastAPI() 
app.include_router(employee_router.router)